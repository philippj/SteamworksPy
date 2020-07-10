"""
Basic example on how to instance a STEAMWORKS API object and execute a basic call
"""

import os
import sys

if sys.version_info >= (3, 8):
  os.add_dll_directory(os.getcwd()) # Required since Python 3.8

from steamworks import STEAMWORKS # Import main STEAMWORKS class

"""
Declare "steamworks" variable and create new instance of the STEAMWORKS class

Depending on failure type this will throw one of following exceptions:
- UnsupportedPlatformException: Platform (sys.platform) not in native supported platforms ['linux', 'linux2', 'darwin', 'win32']
- MissingSteamworksLibraryException: SteamworksPy.* not found in working directory
- FileNotFoundError: steam_appid.txt not found in working directory
OR
Any OS native exception in case of library loading issues
"""
steamworks = STEAMWORKS()

"""
Initialize STEAMWORKS API. This method requires Steam to be running and a user to be logged in.

Depending on failure type this will throw one of following exceptions:
- SteamNotLoadedException: STEAMWORKS class has not yet been loaded
- SteamNotRunningException: Steam is not running
- SteamConnectionException: The API connection to Steam could not be established 
- GenericSteamException: A generic exception occured (retry when encountering this)
"""
steamworks.initialize() # This method has to be called in order for the wrapper to become functional!

"""
Execute two basic calls from the SteamUsers interface to retrieve SteamID from logged in user and Steam profile level 
"""
my_steam64 = steamworks.Users.GetSteamID()
my_steam_level = steamworks.Users.GetPlayerSteamLevel()

print(f'Logged on as {my_steam64}, level: {my_steam_level}')
