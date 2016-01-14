#================================================
#  STEAMWORKS TEST FOR PYTHON
#
#  This test just requires one of the compiled
#  SteamPy files, based on operating system
#
#================================================
from steamworks import *

# Initialize Steam
#------------------------------------------------
Steam.Init()

# Test some functions
#------------------------------------------------
print("--- Steam Apps Functions --------------------------------------")
print("DLC Count: %s") % (SteamApps.GetDlcCount())
print("DLC Installed? (Needs DLC App ID): %s") % (SteamApps.IsDlcInstalled())
print("App Proof of Purchase Key: %s") % (SteamApps.RequestAppProofOfPurchaseKey())
print("--- Steam Friends Functions -----------------------------------")
print("Friend Count: %s") % (SteamFriends.GetFriendCount())
print("Player Name: %s") % (SteamFriends.GetPlayerName())
print("Player State: %s") % (SteamFriends.GetPlayerState())
print("--- Steam Music Functions -------------------------------------")
print("Steam Music On?: %s") % (SteamMusic.MusicIsEnabled())
print("Steam Music Playing?: %s") % (SteamMusic.MusicIsPlaying())
print("System Volume: %s") % (SteamMusic.MusicGetVolume())
print("--- Steam User Functions --------------------------------------")
print("Steam ID: %s") % (SteamUser.GetPlayerID())
print("Steam Level: %s") % (SteamUser.GetPlayerSteamLevel())
print("--- Steam Utility Functions -----------------------------------")
print("Current Battery: %s") % (SteamUtilities.GetCurrentBatteryPower())
print("IP Country: %s") % (SteamUtilities.GetIPCountry())
print("Since App Started: %s") % (SteamUtilities.GetSecondsSinceAppActive())
print("Since Computer Started: %s") % (SteamUtilities.GetSecondsSinceComputerActive())
print("Server Real Time: %s") % (SteamUtilities.GetServerRealTime())
print("Steam Overlay Enabled?: %s") % (SteamUtilities.IsOverlayEnabled())
print("Steam VR Running?: %s") % (SteamUtilities.IsSteamRunningInVR())
print("Steam UI Language: %s") % (SteamUtilities.GetSteamUILanguage())
print("Steam App ID: %s") % (SteamUtilities.GetAppID())
# Test Finished
#------------------------------------------------
print("--- Steam API Test Done ---------------------------------------")