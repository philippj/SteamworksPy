#################################################
#  STEAMWORKS API TEST FOR PYTHON
#
#  This test just requires one of the compiled
#  SteamPy files, based on operating system
#
#################################################
import os, sys, time
from ctypes import *

# Include the Steam API
#################################################
os.environ['LD_LIBRARY_PATH'] = os.getcwd()
# Loading Steam API for Linux
if sys.platform == 'linux' or sys.platform == 'linux2':
	S_API = CDLL(os.path.join(os.getcwd(), "SteamworksPy.so"))
	print("SteamworksPy loaded for Linux")
# Loading Steam API for Mac
elif sys.platform == 'darwin':
	S_API = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dylib"))
	print("SteamworksPy loaded for Mac")
# Loading Steam API for Windows
elif sys.platform == 'win32':
	S_API = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dll"))
	print("SteamworksPy loaded for Windows")
# Unrecognized platform, warn user and do not load Steam API
else:
	print("SteamworksPy failed to load (unsupported platform")

# Set restype for various functions
#################################################
S_API.IsSteamRunning.restype = c_bool
# Steam Apps
S_API.GetDlcCount.restype = int
S_API.IsDlcInstalled.restype = bool
S_API.RequestAppProofOfPurchaseKey.restype = c_char_p
# Steam Friends
S_API.GetFriendCount.restype = int
S_API.GetPersonaName.restype = c_char_p
S_API.GetPersonaState.restype = int
S_API.ActivateGameOverlay.restype = c_char_p
# Steam Music
S_API.MusicIsEnabled.restype = bool
S_API.MusicIsPlaying.restype = bool
S_API.MusicGetVolume.restype = c_float
S_API.MusicPause.restype = None
S_API.MusicPlay.restype = None
S_API.MusicPlayNext.restype = None
S_API.MusicPlayPrev.restype = None
S_API.MusicSetVolume.restype = c_float
# Steam User
S_API.GetSteamID = int
S_API.GetPlayerSteamLevel = int
# Steam User Stats
S_API.GetAchievement.restype = bool
S_API.GetStatFloat.restype = c_float
S_API.GetStatInt.restype = int
S_API.RequestCurrentStats.restype = bool
S_API.SetAchievement.restype = bool
S_API.SetStatFloat.restype = bool
S_API.SetStatInt.restype = bool
S_API.StoreStats.restype = bool
S_API.ClearAchievement.restype = bool
# Steam Utilities
S_API.GetCurrentBatteryPower.restype = int
S_API.GetIPCountry.restype = c_char_p
S_API.GetSecondsSinceAppActive.restype = int
S_API.GetSecondsSinceComputerActive.restype = int
S_API.GetServerRealTime.restype = int
S_API.IsOverlayEnabled.restype = bool
S_API.IsSteamRunningInVR.restype = bool
S_API.GetSteamUILanguage.restype = c_char_p
S_API.GetAppID.restype = int

# Begin testing
#################################################
# Check if Steam is running
if S_API.IsSteamRunning():
	print("Steam is running.")
else:
	print("Steam is not running.")
# Initialize the Steam API
S_API.SteamInit()

# Test that ish
#################################################
STEAM_TEST = True
while STEAM_TEST:
	print("--- Steamworks API Test -------------------------------------")
	print("Which test do you want to use?")
	print("(A)pps, (F)riends, (M)usic, (U)ser, User (S)tats, U(t)ilities, (Q)uit")
	LOOP = raw_input("Run which test?: ")
	# Running apps test
	if LOOP == 'A' or LOOP == 'a':
		print("")
		print(".....running app test.....")
		print("DLC Count: "+str(S_API.GetDlcCount()))
		print("DLC Installed? (Needs DLC App ID): %s") % (S_API.IsDlcInstalled())
		print("App Proof of Purchase Key (If app has serial key): %s") % (S_API.RequestAppProofOfPurchaseKey())
		print(".....app test done.....")
		print("")
	elif LOOP == 'F' or LOOP == 'f':
		print("")
		print(".....running friends test.....")
		print("Friend Count: %s") % (S_API.GetFriendCount())
		print("Player Name: %s") % (S_API.GetPersonaName())
		print("Player State: %s") % (S_API.GetPersonaState())
		print(".....friends test done.....")
		print("")
	elif LOOP == 'M' or LOOP == 'm':
		print("")
		print(".....running music test.....")
		print("Music Enabled?: "+str(S_API.MusicIsEnabled()))
		print("Music Playing?: "+str(S_API.MusicIsPlaying()))
		print("Music Volume: "+str(S_API.MusicGetVolume()))
		print("Attempting to play music...")
		S_API.MusicPlay()
		time.sleep(3)
		print("Attempting to pause music...")
		S_API.MusicPause()
		time.sleep(3)
		print("Attempting to play next song...")
		S_API.MusicPlayNext()
		time.sleep(3)
		print("Attempting to play previous song...")
		S_API.MusicPlayPrev()
		time.sleep(3)
		print("Setting volume to 5...")
		S_API.MusicSetVolume(5)
		time.sleep(3)
		print(".....music test done.....")
		print("")
	elif LOOP == 'U' or LOOP == 'u':
		print("")
		print(".....running user test.....")
		print("Steam ID: %s") % (S_API.GetSteamID())
		print("Steam Level: %s") % (S_API.GetPlayerSteamLevel())
		print(".....user test done.....")
		print("")
	elif LOOP == 'S' or LOOP == 's':
		print("")
		print(".....running stats test.....")
		print("For real though, stat testing should only be done in dev as it will really mess up your Steam stats for the current application/game")
		print(".....stats test done.....")
		print("")
	elif LOOP == 'T' or LOOP == 't':
		print("")
		print(".....running utilities test.....")
		print("Computer Battery Power: "+str(S_API.GetCurrentBatteryPower()))
		print("User Country: "+str(S_API.GetIPCountry()))
		print("Seconds Since Game Active: "+str(S_API.GetSecondsSinceAppActive()))
		print("Seconds Since Computer Active: "+str(S_API.GetSecondsSinceComputerActive()))
		print("Server Time: "+str(S_API.GetServerRealTime()))
		print("Steam Overlay Enabled?: %s") % (S_API.IsOverlayEnabled())
		print("Steam VR Running?: %s") % (S_API.IsSteamRunningInVR())
		print("Steam UI Language: %s") % (S_API.GetSteamUILanguage())
		print("Steam App ID: %s") % (S_API.GetAppID())
		print(".....utilities test done.....")
		print("")
	elif LOOP == 'Q' or LOOP == 'q':
		break
	else:
		pass