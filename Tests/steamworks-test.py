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
print("DLC Count: %s") % (SteamApps.GetDLCCount())
print("Friend Count: %s") % (SteamFriends.GetFriendCount())
print("Player Name: %s") % (SteamFriends.GetPlayerName())
print("Player State: %s") % (SteamFriends.GetPersonaState())
print("Steam ID: %s") % (SteamUser.GetPlayerID())
print("Steam Music On?: %s") % (SteamMusic.IsEnabled())
print("Steam Music Playing?: %s") % (SteamMusic.IsPlaying())
print("System Volume: %s") % (SteamMusic.GetVolume())
print("Current Battery: %s") % (SteamUtils.GetCurrentBatteryPower())
print("IP Country: %s") % (SteamUtils.GetIPCountry())
print("Since App Started: %s") % (SteamUtils.GetSecondsSinceAppActive())
print("Since Computer Started: %s") % (SteamUtils.GetSecondsSinceComputerActive())
print("Server Real Time: %s") % (SteamUtils.GetServerRealTime())
print("Steam Overlay Enabled?: %s") % (SteamUtils.IsOverlayEnabled())
print("Steam VR Running?: %s") % (SteamUtils.IsSteamRunningInVR())