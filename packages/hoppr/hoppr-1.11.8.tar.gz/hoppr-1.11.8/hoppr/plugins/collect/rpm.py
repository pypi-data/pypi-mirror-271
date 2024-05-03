"""
Collector plugin for RPM packages
"""
from __future__ import annotations

import gzip
import time
import warnings

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, MutableMapping

import jmespath
import requests
import xmltodict

from pydantic import SecretStr
from requests import HTTPError, Response
from requests.auth import HTTPBasicAuth

import hoppr.net
import hoppr.utils

from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_process, hoppr_rerunner
from hoppr.constants import BomProps
from hoppr.exceptions import HopprExperimentalWarning, HopprPluginError
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.manifest import SearchSequence
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL


warnings.filterwarnings(action="once", category=HopprExperimentalWarning)
warnings.warn(
    message="The RPM collector plugin is experimental; use at your own risk.",
    category=HopprExperimentalWarning,
    stacklevel=2,
)


class CollectRpmPlugin(SerialCollectorPlugin):
    """
    Collector plugin for RPM packages
    """

    REQUEST_RETRIES: Final[int] = 3
    REQUEST_RETRY_INTERVAL: Final[float] = 5
    REQUEST_TIMEOUT: Final[float] = 60

    products: list[str] = ["rpm/*"]
    required_commands = []
    supported_purl_types: list[str] = ["rpm"]
    system_repositories: list[str] = []

    rpm_data: MutableMapping[str, OrderedDict[str, Any]] = {}

    def get_version(self) -> str:
        return hoppr.__version__

    def _check_artifact_hash(self, dest_file: Path, hash_algorithm: str, hash_string: str):
        computed_hash = hoppr.net.get_file_hash(artifact=dest_file, algorithm=hash_algorithm)

        if computed_hash != hash_string:
            self.get_logger().debug("Computed hash: %s, expected: %s", computed_hash, hash_string, indent_level=2)
            raise HopprPluginError(f"Checksum for {Path(dest_file).name} does not match expected hash.")

    def _download_component(self, download_url: str, dest_file: Path, creds: CredentialRequiredService | None = None):
        self.get_logger().info(msg="Downloading RPM package:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {dest_file}", indent_level=3)

        # Download the RPM file to the target directory
        response = hoppr.net.download_file(  # pylint: disable=duplicate-code
            url=download_url,
            dest=str(dest_file),
            creds=creds,
            proxies=self._get_proxies_for(download_url),
        )

        if not (download_result := Result.from_http_response(response=response)).is_success():
            raise HopprPluginError(download_result.message)

    def _get_download_url(self, purl: PackageURL, repo_url: str) -> tuple[str, str, str]:
        """Get information required to download and verify an RPM package.

        Args:
            purl: PackageURL of component attributes
            repo_url: The RPM repository URL

        Returns:
            Tuple containing download URL, hash algorithm, and checksum string.

        Raises:
            HopprPluginError: malformed/missing `purl.version`, or component not found in repodata
        """
        try:
            rpm_version, rpm_release = purl.version.split("-")
        except (AttributeError, ValueError) as ex:
            raise HopprPluginError(f"Failed to parse version string from PURL: '{purl}'") from ex

        arch = purl.qualifiers.get("arch") or "noarch"

        if (check_result := self.check_purl_specified_url(purl, repo_url)).is_fail():
            if self.context.strict_repos:
                raise HopprPluginError(check_result.message)

            repo_url = purl.qualifiers.get("repository_url", repo_url)
            self._populate_rpm_data(RepositoryUrl(url=repo_url))

        self.get_logger().debug("Searching RPM data for package with attributes:", indent_level=2)
        self.get_logger().debug("name:    %s", purl.name, indent_level=3)
        self.get_logger().debug("version: %s", rpm_version, indent_level=3)
        self.get_logger().debug("release: %s", rpm_release, indent_level=3)
        self.get_logger().debug("arch:    %s", arch, indent_level=3)

        component_data = jmespath.search(
            expression=f"""
                metadata.package[? name=='{purl.name}' &&
                version."@ver"=='{rpm_version}' &&
                version."@rel"=='{rpm_release}' &&
                (arch=='{arch}' || arch=='noarch')] | [0]
            """,
            data=self.rpm_data[repo_url],
        )

        if not component_data:
            raise HopprPluginError(f"RPM package not found in repository: '{purl}'")

        download_url, hash_algorithm, hash_string = jmespath.search(
            expression='[location."@href", checksum."@type", checksum."#text"]',
            data=component_data,
        )

        download_url = f"{repo_url}/{download_url}"

        return download_url, hash_algorithm, hash_string

    def _get_primary_xml_data(
        self,
        repo_url: RepositoryUrl,
        repomd_dict: OrderedDict[str, Any],
        auth: HTTPBasicAuth | None = None,
    ) -> OrderedDict[str, Any]:
        primary_xml_url = jmespath.search(
            expression="""repomd.data[? "@type"=='primary'].location."@href" | [0]""",
            data=repomd_dict,
        )

        primary_xml_url = repo_url / primary_xml_url

        try:
            response = self._stream_url_data(url=primary_xml_url, auth=auth)
        except HTTPError as ex:
            raise HopprPluginError(f"Failed to get primary XML data from {primary_xml_url}") from ex

        data: OrderedDict[str, Any] = OrderedDict()

        # Parse primary XML data to dict
        for chunk in response.iter_content(chunk_size=None):
            data = xmltodict.parse(xml_input=gzip.decompress(chunk), force_list=["package"])

        return data

    def _get_repodata(self, repo_url: RepositoryUrl, auth: HTTPBasicAuth | None = None) -> OrderedDict[str, Any]:
        repomd_url = repo_url / "repodata" / "repomd.xml"

        try:
            response = self._stream_url_data(url=repomd_url, auth=auth)
        except HTTPError as ex:
            raise HopprPluginError(f"Failed to get repository metadata from {repo_url}") from ex

        repomd_dict: OrderedDict[str, Any] = xmltodict.parse(xml_input=response.text, force_list=["data"])

        # Download all metadata files listed in repomd.xml to bundle directory for this repo
        metadata_files = jmespath.search(expression='repomd.data[].location."@href"', data=repomd_dict)
        repodata_dir = self.directory_for(purl_type="rpm", repo_url=str(repo_url), subdir="repodata")

        for metadata_file in metadata_files:
            self.get_logger().debug("Downloading %s", metadata_file, indent_level=2)
            hoppr.net.download_file(url=str(repo_url / metadata_file), dest=str(repodata_dir.parent / metadata_file))

        return repomd_dict

    def _populate_rpm_data(self, repo_url: RepositoryUrl) -> None:
        """
        Populate `rpm_data` dict for a repository

        Args:
            repo_url (str): The RPM repository URL
        """
        if type(self).rpm_data.get(f"{repo_url}"):
            return

        self.get_logger().debug("Populating RPM data for repository: %s", repo_url, indent_level=1)

        auth: HTTPBasicAuth | None = None

        if (creds := Credentials.find(f"{repo_url}")) and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

        try:
            repomd_dict: OrderedDict[str, Any] = self._get_repodata(repo_url, auth=auth)
            primary_xml_data: OrderedDict[str, Any] = self._get_primary_xml_data(repo_url, repomd_dict, auth)
        except HopprPluginError as ex:
            raise ex

        type(self).rpm_data[f"{repo_url}"] = primary_xml_data

    def _stream_url_data(self, url: RepositoryUrl, auth: HTTPBasicAuth | None = None) -> Response:
        """Stream download data from specified URL.

        Args:
            url: URL of remote resource to stream.
            auth: Basic authentication if required by URL. Defaults to None.

        Raises:
            HTTPError: Failed to download resource after 3 attempts.

        Returns:
            The web request response.
        """
        response = Response()

        for _ in range(self.REQUEST_RETRIES):
            response = requests.get(
                url=f"{url}",
                auth=auth,
                stream=True,
                timeout=self.REQUEST_TIMEOUT,
                proxies=self._get_proxies_for(f"{url}"),
            )

            try:
                response.raise_for_status()
                return response
            except HTTPError:
                time.sleep(self.REQUEST_RETRY_INTERVAL)

        raise HTTPError(f"Failed to retrieve data from {url}", response=response)

    @hoppr_process
    @hoppr_rerunner
    def pre_stage_process(self) -> Result:
        """
        Populate RPM data mapping for repositories
        """
        # Get all repository search sequences from all components
        results: list[str] = jmespath.search(
            expression=f"""
                components[*] | [? starts_with(purl, 'pkg:rpm')].properties[] |
                [? name=='{BomProps.COMPONENT_SEARCH_SEQUENCE.value}'].value
            """,
            data=self.context.consolidated_sbom.dict(),
        )

        # Parse and flatten repositories from component search sequence JSON strings, then remove duplicates
        search_repos = [repo for result in results for repo in SearchSequence.parse_raw(result).repositories]
        search_repos = hoppr.utils.dedup_list(search_repos)

        for repo_url in [RepositoryUrl(url=url) for url in search_repos]:
            self._populate_rpm_data(repo_url)

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)

        try:
            download_url, hash_algorithm, hash_string = self._get_download_url(purl=purl, repo_url=repo_url)
        except HopprPluginError as ex:
            return Result.retry(message=str(ex))

        target_dir = self.directory_for(
            purl_type="rpm",
            repo_url=repo_url,
            subdir=Path(download_url).parent.relative_to(repo_url),
        )

        dest_file = target_dir / Path(download_url).name

        try:
            self._download_component(download_url, dest_file, creds)
            self._check_artifact_hash(dest_file, hash_algorithm, hash_string)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, target_dir)

        return Result.success(return_obj=comp)
