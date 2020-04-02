#================================================
#  STEAMWORKS TEST FOR PYTHON
#================================================
#
#  This test just requires one of the compiled
#  SteamworksPy files, based on operating system
#
#================================================
from steamworks import *
import time
#------------------------------------------------
# Initialize Steam
#------------------------------------------------
Steam.Init()
#------------------------------------------------
# Test Steam Apps functions
def appsTest():
	print("\n#------------------------------------------------\nINFO: Running apps test.....\n")
	print("Has Other App/Game (using Spacewars): %s") % (SteamApps.HasOtherApp(480))
	print("DLC Count: %s") % (SteamApps.GetDlcCount())
	print("Is App/Game Installed? (using Spacewars): %s") % (SteamApps.IsAppInstalled(480))
	print("Current Game Language: %s") % (SteamApps.GetCurrentGameLanguage())
	raw_input("\nINFO: Apps test done. Press any key to continue.\n")
#------------------------------------------------
# Test Steam Friends functions
def friendsTest():
	print("\n#------------------------------------------------\nINFO: Running friends test.....\n")
	print("Friend Count: %s") % (SteamFriends.GetFriendCount())
	print("Player Name: %s") % (SteamFriends.GetPlayerName())
	print("Player State: %s") % (SteamFriends.GetPlayerState())
	print("Friend's Name (using Gramps): %s") % (SteamFriends.GetFriendPersonaName(76561198002965952))
	raw_input("INFO: Friends test done. Press any key to continue.\n")
#------------------------------------------------
# Test Steam Music functions
def musicTest():
	print("\n#------------------------------------------------\nINFO: Running music test.....\n")
	print("Music Enabled?: "+str(SteamMusic.MusicIsEnabled()))
	print("Music Playing?: "+str(SteamMusic.MusicIsPlaying()))
	print("Music Volume: "+str(SteamMusic.MusicGetVolume()))
	print("Attempting to play music...")
	SteamMusic.MusicPlay()
	time.sleep(3)
	print("Attempting to pause music...")
	SteamMusic.MusicPause()
	time.sleep(3)
	print("Attempting to play next song...")
	SteamMusic.MusicPlayNext()
	time.sleep(3)
	print("Attempting to play previous song...")
	SteamMusic.MusicPlayPrev()
	time.sleep(3)
	print("Setting volume to 5...")
	SteamMusic.MusicSetVolume(5)
	time.sleep(3)
	raw_input("INFO: Music test done. Press any key to continue.\n")
#------------------------------------------------
# Test Steam Users functions
def userTest():
	print("\n#------------------------------------------------\nINFO: Running user test.....\n")
	print("Steam ID: %s") % (SteamUser.GetPlayerID())
	print("Steam Level: %s") % (SteamUser.GetPlayerSteamLevel())
	print("Steam User Folder: %s") % (SteamUser.GetUserDataFolder())
	raw_input("INFO: User test done. Press any key to continue.\n")
#------------------------------------------------
# Test Steam User Stats functions
def statsTest():
	print("\n#------------------------------------------------\nINFO: Running stats test.....\n")
	print("This test only works in a game with statistics and achievements enabled. Sorry!")
	raw_input("INFO: Stats test done. Press any key to continue.\n")
#------------------------------------------------
# Test Steam Utilities functions
def utilitiesTest():
	print("\n#------------------------------------------------\nINFO: Running utilities test.....\n")
	print("Computer Battery Power: "+str(SteamUtilities.GetCurrentBatteryPower()))
	print("User Country: "+str(SteamUtilities.GetIPCountry()))
	print("Seconds Since Game Active: "+str(SteamUtilities.GetSecondsSinceAppActive()))
	print("Seconds Since Computer Active: "+str(SteamUtilities.GetSecondsSinceComputerActive()))
	print("Server Time: "+str(SteamUtilities.GetServerRealTime()))
	print("Steam Overlay Enabled?: %s") % (SteamUtilities.IsOverlayEnabled())
	print("Steam VR Running?: %s") % (SteamUtilities.IsSteamRunningInVR())
	print("Steam UI Language: %s") % (SteamUtilities.GetSteamUILanguage())
	print("Steam App ID: %s") % (SteamUtilities.GetAppID())
	raw_input("INFO: Utilities test done. Press any key to continue.\n")
#------------------------------------------------
# The main test loop
#------------------------------------------------
# Set some variables
STEAM_TEST = True
FIRST_RUN = False
# The loop itself
while STEAM_TEST:
	if FIRST_RUN == False:
		print("##################################################\nSTEAMWORKS PYTHON API TEST\n##################################################\n")
		print("This will loop through different sections of the SteamworksPy API system for testing purposes.\n")
		print("Some functions are omitted as they will not work properly without being in a game, transmitting data, or inputting the ID's, etc.\n")
		print("Please try these functions out in your own game and report any issues you find.\n")
	print("Which test do you want to use?\n")
	print("(A)pps, (F)riends, (M)usic, (U)ser, User (S)tats, U(t)ilities, (Q)uit")
	LOOP = raw_input("Run which test?: ")
	# Running apps test
	if LOOP == 'A' or LOOP == 'a':
		appsTest()
	elif LOOP == 'F' or LOOP == 'f':
		friendsTest()
	elif LOOP == 'M' or LOOP == 'm':
		musicTest()
	elif LOOP == 'U' or LOOP == 'u':
		userTest()
	elif LOOP == 'S' or LOOP == 's':
		statsTest()
	elif LOOP == 'T' or LOOP == 't':
		utilitiesTest()
	elif LOOP == 'Q' or LOOP == 'q':
		break
	else:
		pass