#================================================
#  STEAMWORKS API TEST FOR PYTHON
#
#  This test just requires one of the compiled
#  SteamPy files, based on operating system
#
#================================================
import os, sys
from ctypes import *

# Include the Steam API
#------------------------------------------------
os.environ['LD_LIBRARY_PATH'] = os.getcwd()
# Loading Steam API for Linux
if sys.platform == 'linux' or sys.platform == 'linux2':
	S_API = CDLL(os.path.join(os.getcwd(), "libsteampy.so"))
	print("Steam API loaded for Linux")
# Loading Steam API for Mac
elif sys.platform == 'darwin':
	S_API = CDLL(os.path.join(os.getcwd(), "libsteampy.dylib"))
	print("Steam API loaded for Mac")
# Loading Steam API for Windows
elif sys.platform == 'win32':
	S_API = CDLL(os.path.join(os.getcwd(), "steampy.dll"))
	print("Steam API loaded for Windows")
# Unrecognized platform, warn user and do not load Steam API
else:
	print("Steam API failed to load (unsupported platform")

# Set restype for various functions
#------------------------------------------------
S_API.SteamAPI_IsSteamRunning.restype = c_bool
# Steam Apps
S_API.GetDLCCount.restype = int
S_API.IsDlcInstalled.restype = bool
# Steam Friends
S_API.GetFriendCount.restype = int
S_API.GetPersonaName.restype = c_char_p
S_API.GetPersonaState.restype = int
# Steam Music
S_API.MusicIsEnabled.restype = bool
S_API.MusicIsPlaying.restype = bool
S_API.MusicGetVolume.restype = c_float
# Steam User
S_API.GetSteamID = int
# Steam User Stats
S_API.GetAchievement.restype = bool
S_API.GetStatFloat.restype = c_float
S_API.GetStatInt.restype = int
S_API.RequestCurrentStats.restype = bool
S_API.SetAchievement.restype = bool
S_API.SetStatFloat.restype = bool
S_API.SetStatInt.restype = bool
S_API.StoreStats.restype = bool
# Steam Utilities
S_API.GetCurrentBatteryPower.restype = int
S_API.GetIPCountry.restype = c_char_p
S_API.GetSecondsSinceAppActive.restype = int
S_API.GetSecondsSinceComputerActive.restype = int
S_API.GetServerRealTime.restype = int
S_API.IsOverlayEnabled.restype = bool
S_API.IsSteamRunningInVR.restype = bool

# Begin testing
#------------------------------------------------
# Check if Steam is running
if S_API.SteamAPI_IsSteamRunning():
	print("Steam is running.")
else:
	print("Steam is not running.")
# Initialize the Steam API
S_API.SteamInit()

# Test that ish
#------------------------------------------------
print(S_API.GetDLCCount())
print(S_API.GetPersonaName())
print(S_API.GetIPCountry())
print(S_API.MusicIsEnabled())
print(S_API.MusicIsPlaying())
print(S_API.MusicGetVolume())
print(S_API.GetCurrentBatteryPower())
print(S_API.GetSecondsSinceAppActive())
print(S_API.GetSecondsSinceComputerActive())
print(S_API.GetServerRealTime())
print(S_API.IsSteamRunningInVR())