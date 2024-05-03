"""Install 'Chrome for Testing' assets from the stable channel.

By default, if none specified, the latest version of assets, compatible
binaries of 'Chrome for Testing' and chromedriver, are installed. Different
versions of assets will be installed in their own
'${HOME}/.c4t-assets/<version>' directory. Once a version is
successfully installed it will be the 'active' version by symlinking
'${HOME}/.c4t-assets/chrome' and '${HOME}/.c4t-assets/chromedriver'
to the last installed version of
assets in '${HOME}/.c4t-assets/<version>/chrome-linux64/chrome' and
'${HOME}/.c4t-assets/<version>/chromedriver-linux64/chromedriver' respectively.
Installing the 'active' version of assets again will not touch the installation
of that version. The same goes for installing a previously installed version
except that it will change the symlinks in '${HOME}/.c4t-assets/' to the assets
of that version, effectively making that version 'active'.

N.B: Currently installs assets for linux64 platform only

usage:

    import c4t
    from selenium.webdriver import ChromeOptions, ChromeService, Chrome

    version = ''
    assets = c4t.Assets()
    assets.install(version) if version else assets.install()

    options = ChromeOptions()
    options.binary_location = c4t.location.chrome
    service = ChromeService(executable_path=c4t.location.chromedriver)
    browser = Chrome(options=options, service=service)
    browser.get('https://pypi.org/user/p4irin/')
    browser.close()
    browser.quit()
"""


__author__ = 'p4irin'
__email__ = '139928764+p4irin@users.noreply.github.com'
__version__ = '1.5.0'


import requests
import os
import json
import wget
import zipfile
from typing import Literal, List, Union


_default_path_to_assets = f'{os.environ["HOME"]}/.c4t-assets'
_path_to_assets = os.getenv(
    'C4T_PATH_TO_ASSETS', _default_path_to_assets
)


class _Location:
    """Specify the location/path to the assets' binaries.
    
    Attributes:
        chrome: The path to the 'Chrome for Testing' binary
        chromedriver: The path to the chromedriver binary
    """
    chrome: str = f'{_path_to_assets}/chrome'
    chromedriver: str = f'{_path_to_assets}/chromedriver'


location = _Location


class UnknownChromeVersion(Exception):
    """Raised when the version of Chrome for Testing is unknown."""
    pass


class ChromedriverVersionDoesNotExist(Exception):
    """No chromedriver exists for corresponding Chrome for testing version."""
    pass


class Assets(object):
    """Install and manage 'Chrome for Testing' assets."""

    _base_url = 'https://googlechromelabs.github.io/chrome-for-testing'
    _last_known_good_versions_json_api_endpoint = (
        f"{_base_url}/last-known-good-versions-with-downloads.json"
    )
    _known_good_versions_json_api_endpoint = (
        f'{_base_url}/known-good-versions-with-downloads.json'
    )
    _successful_installation_message = """
Finished installing version {version} of Chrome for Testing and Chromedriver.
-------------------------------------------
Version {version} is the active version.
-------------------------------------------

Usage:

from selenium.webdriver import ChromeOptions, ChromeService, Chrome
import c4t

options = ChromeOptions()
options.binary_location = c4t.location.chrome
service = ChromeService(executable_path=c4t.location.chromedriver)
browser = Chrome(options=options, service=service)
browser.get('https://pypi.org/user/p4irin/')
browser.close()
browser.quit()
"""

    def __init__(self) -> None:
        """Create the root directory for assets and initialize attributes."""
        self._create_assets_dir()
        self._platform = ''
        self._download_dir = ''

    def _create_assets_dir(self) -> None:
        """Create the installation directory for multiple versions of assets.

        Raises:
            SystemExit on unhandled exceptions.
        """
        try:
            os.mkdir(_path_to_assets)
        except FileExistsError:
            pass
        except Exception as e:
            raise SystemExit(e)
        
    def _installation_path_of(
            self, binary: Literal['chrome', 'chromedriver']
        ) -> str:
        """Returns the installation path of the binary.
        
        Args:
            binary: Which binary should the path be for?
        """

        return f'{self._download_dir}/{binary}-{self._platform}'
        
    def _make_executable(
            self, files: List[str],
            for_binary: Literal['chrome', 'chromedriver']
        ) -> None:
        """Set the execute bit on each file in a list.
        
        Necessary, zipfile doesn't preserve file permissions.

        Args:
            files: Files that should have their execute bit on.
            for_binary: The binary the files are related to.
        """

        for file in files:
            try:
                os.chmod(f'{self._installation_path_of(for_binary)}/{file}', 0o755)
            except FileNotFoundError:
                # Some files were removed from the Chrome zip download
                # Just move on to the next file
                continue

    def _download(
            self,
            binary: Literal['chrome', 'chromedriver'],
            for_platform: str,
            from_url: str
        ) -> str:
        """Download the binary for a platform.
        
        Currently only for linux64 platform.

        Args:
            binary:
            for_platform:
            from_url:

        Returns:
            The name of the zip file of the binary.

        Raises:
            An unhandled exception if downloading fails.
        """

        binary_zip_file = f'{binary}-{for_platform}.zip'
        binary_zip_file_path = f'{self._download_dir}/{binary_zip_file}'
        if os.path.isfile(f'{binary_zip_file_path}'):
            print(f'{binary_zip_file} exists. Skipping download.')
            return binary_zip_file
        print(f'Downloading {binary_zip_file}.')
        try:
            wget.download(from_url, self._download_dir)
            print('\n')
        except Exception as e:
            print(f'wget threw Exception {e}')
            raise e
        return binary_zip_file
    
    def extract_zip_with_permissions(self, zip_file: str, destination: str):
        """Extract zip file and keep file permissions
        
        zipfile doesn't keep file permissions

        Args:
            zip_file: Relative path from working directory to the zip file
            destination: Relative path from working directory
        """
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for member in zip_ref.infolist():
                zip_ref.extract(member, destination)
                file_name = f'{destination}/{member.filename}'
                permissions = member.external_attr >> 16
                os.chmod(file_name, permissions)    

    def _unzip(
            self,
            binary: Literal['chrome', 'chromedriver'],
            from_zip_file: str,
            for_platform: str='linux64'
        ) -> None:
        """Extract the files related to a binary from the zip file.
        
        Args:
            binary: The binary the zip file is for.
            from_zip_file: The name of the zip file to extract the binary's
                files from.
            for_platform: The binary's target platform. Currently only linux64.
        """

        print(f'Unzipping {from_zip_file}')
        binary_path = f'{self._download_dir}/{binary}-{for_platform}/{binary}'
        if os.path.isfile(binary_path):
            print(f'{from_zip_file} already unzipped. Skipping')
        else:
            self.extract_zip_with_permissions(
                f'{self._download_dir}/{from_zip_file}', f'{self._download_dir}'
            )

    def _create_symlink(
            self,
            to_binary: Literal['chrome', 'chromedriver'],
            version: str,
            for_platform: str='linux64'
        ) -> None:
        """Create symlink to the installed binary.

        Args:
            to_binary: The name of the binary to create a symlink to.
            version: The version of the binary to symlink to.
            for_platform: The binary's target platform. Currently only linux64.
        """
        symlink_to_binary = f'{_path_to_assets}/{to_binary}'
        if os.path.islink(symlink_to_binary):
            link_target = os.readlink(symlink_to_binary)
            if version not in link_target.split('/'):
                os.remove(symlink_to_binary)

        if not os.path.islink(symlink_to_binary):
            print(
                f'Creating symlink to {to_binary} version {version}'
            )
            os.symlink(
                f'./{version}/{to_binary}-{for_platform}/{to_binary}',
                f'{_path_to_assets}/{to_binary}'
            )
            return
        
        if version in link_target.split('/'):
            print(
                f'Symlink for {to_binary} version {version} already ' +
                'exists. Skipping'
            )

    @property
    def active_version(self) -> Union[str, bool]:
        """The active version of 'Chrome for Testing' assets installed.
        
        Returns:
            str: Representing the active version.
            bool: False. No installed version was found.
        """
        symlink_to_chrome = f'{_path_to_assets}/chrome'
        try:
            version = os.readlink(symlink_to_chrome).split('/')[1]
            return version
        except FileNotFoundError:
            print(f'Symlink {symlink_to_chrome} not found!')
            print('Make sure you install a version of assets first!')
            return False
        
    def install(self, version: str='latest', platform: str='linux64') -> None:
        """Install either the default latest or a specific stable version.
        
        Args:
            version: The version of assets to install.
            platform: The target platform. Currently only 'linux64'.

        Raises:
            RequestException: The request to the json api endpoint failed.
            ChromedriverVersionDoesNotExist: There's no download for the
                version requested.
            UnknownChromeVersion: There's no download for the requested version
                of 'Chrome for Testing'.
        """
        self._platform = platform

        if version == 'latest':
            json_api_endpoint = (
                self._last_known_good_versions_json_api_endpoint
            )
        else:
            json_api_endpoint = self._known_good_versions_json_api_endpoint

        try:
            r = requests.get(json_api_endpoint)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        json_response = json.loads(r.text)
        if version == 'latest':
            stable_channel = json_response['channels']['Stable']
            version = stable_channel['version']
            chrome_downloads = stable_channel['downloads']['chrome']
            chromedriver_downloads = (
                stable_channel['downloads']['chromedriver']
            )
        else:
            versions = json_response['versions']
            found_version = False
            for a_version in versions:
                if a_version['version'] == version:
                    chrome_downloads = a_version['downloads']['chrome']
                    try:
                        chromedriver_downloads = (
                            a_version['downloads']['chromedriver']
                        )
                    except KeyError:
                        raise ChromedriverVersionDoesNotExist
                    found_version = True
                    break
            if not found_version:
                raise UnknownChromeVersion

        self._download_dir = f'{_path_to_assets}/{version}'
        print(f'Create directory {self._download_dir}')
        try:
            os.makedirs(
                self._download_dir,
                mode=0o775
            )
        except FileExistsError:
            print('Skipping: Directory exists.')

        for chrome in chrome_downloads:
            if chrome['platform'] == platform:
                chrome_zip_file = self._download(
                    binary='chrome',
                    for_platform=platform,
                    from_url=chrome['url']
                )
                break

        for chromedriver in chromedriver_downloads:
            if chromedriver['platform'] == platform:
                chromedriver_zip_file = self._download(
                    binary='chromedriver',
                    for_platform=platform,
                    from_url=chromedriver['url']
                )
                break

        self._unzip(
            binary='chrome', 
            from_zip_file=chrome_zip_file,
            for_platform='linux64'
        )

        self._unzip(
            binary='chromedriver',
            from_zip_file=chromedriver_zip_file,
            for_platform='linux64'
        )

        self._create_symlink(
            to_binary='chrome',
            version=version,
            for_platform='linux64'
        )

        self._create_symlink(
            to_binary='chromedriver',
            version=version,
            for_platform='linux64'
        )

        print(self._successful_installation_message.format(version=version))

    @property
    def path(self) -> str:
        return _path_to_assets

    def installed(self, output: bool=True) -> List[str]:
        """List installed versions"""

        versions = []
        items = [item for item in os.listdir(self.path) if os.path.isdir(f'{self.path}/{item}')]
        items.sort()
        for n, item in enumerate(items, start=0):
            if os.path.isdir(f'{self.path}/{item}'):
                if output:
                    active = ', active' if item == self.active_version else ''
                    print(f'{n} - {item}{active}')
                versions.append(item)
        return versions
    
    def _isinstalled(self, version: str) -> bool:
        installed_versions = self.installed(output=False)
        if version in installed_versions:
            return True
        else:
            return False
    
    def switch(self) -> None:
        """Switch the active version"""

        versions = self.installed()

        try:
            selection = int(input("Select a version by number: "))
        except ValueError:
            selection = None
        except IndexError:
            selection = None

        if selection is not None:
            version = versions[selection]
            self._create_symlink(to_binary='chrome', version=version)
            self._create_symlink(to_binary='chromedriver', version=version)
            print(f'Active version is now: {version}')

    def last_known_good_versions(self) -> List[str]:
        """List last known good versions"""

        versions = []
        try:
            r = requests.get(
                self._last_known_good_versions_json_api_endpoint
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        json_response = json.loads(r.text)
        channels = json_response['channels']
        for n, channel in enumerate(channels, start=0):
            version = channels[channel]['version']
            revision = channels[channel]['revision']
            if self._isinstalled(version):
                installed = ', installed'
            else:
                installed = ''
            print(f'{n} - {channel} version={version}, revision={revision}{installed}')
            versions.append(version)
        return versions
    
    def install_last_known_good_version(self) -> None:
        versions = self.last_known_good_versions()
        try:
            selection = int(input('Select a version by number: '))
        except ValueError:
            selection = None
        except IndexError:
            selection = None

        if selection is not None:
            self.install(version=versions[selection])