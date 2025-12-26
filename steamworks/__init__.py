"""
Copyright (c) 2016 GP Garcia, CoaguCo Industries

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
__version__ = '2.0.0'
__author__  = 'GP Garcia'

import sys, os, time
from ctypes import *
from enum import Enum
from pathlib import Path

import steamworks.util 		as steamworks_util
from steamworks.enums 		import *
from steamworks.structs 	import *
from steamworks.exceptions 	import *
from steamworks.methods 	import STEAMWORKS_METHODS

from steamworks.interfaces.apps         import SteamApps
from steamworks.interfaces.friends      import SteamFriends
from steamworks.interfaces.matchmaking  import SteamMatchmaking
from steamworks.interfaces.music        import SteamMusic
from steamworks.interfaces.screenshots  import SteamScreenshots
from steamworks.interfaces.users        import SteamUsers
from steamworks.interfaces.userstats    import SteamUserStats
from steamworks.interfaces.utils        import SteamUtils
from steamworks.interfaces.workshop     import SteamWorkshop
from steamworks.interfaces.microtxn     import SteamMicroTxn
from steamworks.interfaces.input        import SteamInput

is_nuitka = '__compiled__' in globals()


class STEAMWORKS(object):
    """
    Primary STEAMWORKS class used for fundamental handling of the STEAMWORKS API

    :param supported_platforms: Optional list of platforms to support (restricts initialization)
    :param lib_path: Optional path to directory containing Steamworks libraries
                     (libsteam_api.so/dylib/dll and SteamworksPy.so/dylib/dll)
                     If not provided, searches current directory, package directory, and Nuitka fallback
    """
    _arch = steamworks_util.get_arch()
    _native_supported_platforms = ['linux', 'linux2', 'darwin', 'win32']

    def __init__(
        self,
        supported_platforms: list = [],
        lib_path: str | Path | None = None
    ) -> None:
        self._supported_platforms = supported_platforms
        self._lib_path = lib_path
        self._loaded 	= False
        self._cdll 		= None

        self.app_id 	= 0

        # Set LD_LIBRARY_PATH before loading libraries (Linux/macOS only)
        if sys.platform in ['linux', 'linux2', 'darwin']:
            self._setup_library_path()

        self._initialize()

    def _get_library_search_paths(self) -> list[str]:
        """
        Build ordered list of directories to search for libraries.

        Priority order:
        1. Custom lib_path (if provided)
        2. Current working directory
        3. Package directory
        4. Nuitka fallback (2 dirs up from __file__)

        :return: List of directory paths to search
        """
        paths = []

        # Priority 1: Custom lib_path if provided
        if self._lib_path is not None:
            resolved_path = str(Path(self._lib_path).resolve())
            paths.append(resolved_path)

        # Priority 2: Current working directory
        paths.append(os.getcwd())

        # Priority 3: Package directory
        paths.append(os.path.dirname(__file__))

        # Priority 4: Nuitka fallback (2 dirs up)
        if is_nuitka:
            nuitka_path = os.path.split(os.path.split(__file__)[0])[0]
            paths.append(nuitka_path)

        return paths

    def _find_library(self, filename: str, search_paths: list[str]) -> str | None:
        """
        Search for library file in given paths.

        :param filename: Library filename to find
        :param search_paths: Ordered list of directories to search
        :return: Absolute path to library if found, None otherwise
        """
        for path in search_paths:
            full_path = os.path.join(path, filename)
            if os.path.isfile(full_path):
                return full_path
        return None

    def _setup_library_path(self) -> None:
        """
        Configure LD_LIBRARY_PATH environment variable for library loading.
        Only needed on Linux/macOS.
        """
        # Build path list (custom path gets priority)
        paths_to_add = []

        if self._lib_path is not None:
            paths_to_add.append(str(Path(self._lib_path).resolve()))

        paths_to_add.append(os.getcwd())

        # Preserve existing LD_LIBRARY_PATH
        existing = os.environ.get('LD_LIBRARY_PATH', '')
        if existing:
            paths_to_add.append(existing)

        os.environ['LD_LIBRARY_PATH'] = ':'.join(paths_to_add)

    def _initialize(self) -> bool:
        """Initialize module by loading STEAMWORKS library

        :return: bool
        """
        platform = sys.platform
        if self._supported_platforms and platform not in self._supported_platforms:
            raise UnsupportedPlatformException(f'"{platform}" has been excluded')

        if platform not in STEAMWORKS._native_supported_platforms:
            raise UnsupportedPlatformException(f'"{platform}" is not being supported')

        # Get search paths for library loading
        search_paths = self._get_library_search_paths()

        # Determine library filenames based on platform
        library_file_name = ''
        if platform in ['linux', 'linux2']:
            library_file_name = 'SteamworksPy.so'
            # Load Steam API library (required on Linux)
            steam_api_path = self._find_library('libsteam_api.so', search_paths)
            if steam_api_path:
                cdll.LoadLibrary(steam_api_path)
            else:
                raise MissingSteamworksLibraryException(f'Missing library "libsteam_api.so"')

        elif platform == 'darwin':
            library_file_name = 'SteamworksPy.dylib'

        elif platform == 'win32':
            library_file_name = 'SteamworksPy.dll' if STEAMWORKS._arch == Arch.x86 else 'SteamworksPy64.dll'

        else:
            # This case is theoretically unreachable
            raise UnsupportedPlatformException(f'"{platform}" is not being supported')

        # Load SteamworksPy wrapper library
        library_path = self._find_library(library_file_name, search_paths)
        if not library_path:
            raise MissingSteamworksLibraryException(f'Missing library {library_file_name}')

        # Find steam_appid.txt
        # Check parent of lib_path first (if custom path provided), then search paths
        paths_to_check = []
        if self._lib_path is not None:
            lib_parent = str(Path(self._lib_path).resolve().parent)
            paths_to_check.append(lib_parent)
            paths_to_check.append(str(Path(self._lib_path).resolve()))

        for path in search_paths:
            if path not in paths_to_check:
                paths_to_check.append(path)

        app_id_file = None
        for path in paths_to_check:
            candidate = os.path.join(path, 'steam_appid.txt')
            if os.path.isfile(candidate):
                app_id_file = candidate
                break

        if not app_id_file:
            raise FileNotFoundError(f'steam_appid.txt missing. Searched: {", ".join(paths_to_check)}')

        with open(app_id_file, 'r') as f:
            self.app_id	= int(f.read())

        self._cdll 		= CDLL(library_path) # Throw native exception in case of error
        self._loaded 	= True

        self._load_steamworks_api()
        return self._loaded


    def _load_steamworks_api(self) -> None:
        """Load all methods from steamworks api and assign their correct arg/res types based on method map

        :return: None
        """
        if not self._loaded:
            raise SteamNotLoadedException('STEAMWORKS not yet loaded')

        for method_name, attributes in STEAMWORKS_METHODS.items():
            f = getattr(self._cdll, method_name)

            if 'restype' in attributes:
                f.restype = attributes['restype']

            if 'argtypes' in attributes:
                f.argtypes = attributes['argtypes']

            setattr(self, method_name, f)

        self._reload_steamworks_interfaces()


    def _reload_steamworks_interfaces(self) -> None:
        """Reload all interface classes

        :return: None
        """
        self.Apps           = SteamApps(self)
        self.Friends        = SteamFriends(self)
        self.Matchmaking    = SteamMatchmaking(self)
        self.Music          = SteamMusic(self)
        self.Screenshots    = SteamScreenshots(self)
        self.Users          = SteamUsers(self)
        self.UserStats      = SteamUserStats(self)
        self.Utils          = SteamUtils(self)
        self.Workshop       = SteamWorkshop(self)
        self.MicroTxn       = SteamMicroTxn(self)
        self.Input          = SteamInput(self)


    def initialize(self) -> bool:
        """Initialize Steam API connection

        :return: bool
        """
        if not self.loaded():
            raise SteamNotLoadedException('STEAMWORKS not yet loaded')

        if not self.IsSteamRunning():
            raise SteamNotRunningException('Steam is not running')

        # Boot up the Steam API
        result = self._cdll.SteamInit()
        if result == 2:
            raise SteamNotRunningException('Steam is not running')

        elif result == 3:
            raise SteamConnectionException('Not logged on or connection to Steam client could not be established')

        elif result != 0:
            raise GenericSteamException('Failed to initialize STEAMWORKS API')

        return True

    def relaunch(self, app_id: int) -> bool:
        """

        :param app_id: int
        :return: None
        """
        return self._cdll.RestartAppIfNecessary()

    def unload(self) -> None:
        """Shuts down the Steamworks API, releases pointers and frees memory.

        :return: None
        """
        self._cdll.SteamShutdown()
        self._loaded    = False
        self._cdll      = None


    def loaded(self) -> bool:
        """Is library loaded and everything populated

        :return: bool
        """
        return (self._loaded and self._cdll)


    def run_callbacks(self) -> bool:
        """Execute all callbacks

        :return: bool
        """
        if not self.loaded():
            raise SteamNotLoadedException('STEAMWORKS not yet loaded')

        self._cdll.RunCallbacks()
        return True

    def run_forever(self, base_interval: float = 1.0) -> None:
        """Loop and call Steam.run_callbacks in specified interval

        :param base_interval: float
        :return: None
        """
        while True:
            self.run_callbacks()
            time.sleep(base_interval)
