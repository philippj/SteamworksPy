#================================================
# Steamworks For Python
#================================================
from ctypes import *
import sys, os
#------------------------------------------------
# User Status
#------------------------------------------------
FriendFlags = {  # regular friend
    'None': 0x00,
    'Blocked': 0x01,
    'FriendshipRequested': 0x02,
    'Immediate': 0x04,
    'ClanMember': 0x08,
    'OnGameServer': 0x10,
    'RequestingFriendship': 0x80,
    'RequestingInfo': 0x100,
    'Ignored': 0x200,
    'IgnoredFriend': 0x400,
    'Suggested': 0x800,
    'All': 0xFFFF,
    }
#------------------------------------------------
# Workshop File Types
#------------------------------------------------
WorkshopFileType = {
	'Community': 0x00,			# normal Workshop item that can be subscribed to
	'Microtransaction': 0x01,	# Workshop item that is meant to be voted on for the purpose of selling in-game

	# NOTE: There are more workshop file types defined "in isteamremotestorage.h",
	# but we do not need them for now.
}
#------------------------------------------------
# Workshop Item States
#------------------------------------------------
WorkshopItemState = {
	"ItemStateNone":			0,	# item not tracked on client
	"ItemStateSubscribed":		1,	# current user is subscribed to this item. Not just cached.
	"ItemStateLegacyItem":		2,	# item was created with ISteamRemoteStorage
	"ItemStateInstalled":		4,	# item is installed and usable (but maybe out of date)
	"ItemStateNeedsUpdate":		8,	# items needs an update. Either because it's not installed yet or creator updated content
	"ItemStateDownloading":		16,	# item update is currently downloading
	"ItemStateDownloadPending":	32,	# DownloadItem() was called for this item, content isn't available until DownloadItemResult_t is fired
}
#------------------------------------------------
# Main Steam Class, obviously
#------------------------------------------------
class Steam:
	# Set some basic variables for the Steam class
	cdll = None
	warn = False
	loaded = False
	# Initialize Steam
	@staticmethod
	def Init():
		os.environ['LD_LIBRARY_PATH'] = os.getcwd()
		# Check system architecture
		# This may need refined, might not work so well in Windows
		if (sys.maxsize > 2**32) is False:
			OS_BIT = '32bits'
		else:
			OS_BIT = '64bits'
		# Loading SteamworksPy API for Linux
		if sys.platform == 'linux' or sys.platform == 'linux2':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.so"))
			print("INFO: SteamworksPy loaded for Linux")
			Steam.loaded = True
		# Loading SteamworksPy API for Mac
		elif sys.platform == 'darwin':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dylib" ))
			print("INFO: SteamworksPy loaded for Mac")
			Steam.loaded = True
		# Loading SteamworksPy API for Windows
		elif sys.platform == 'win32':
			# Check Windows architecture
			if OS_BIT == '32bits':
				Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dll"))
			else:
				Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy64.dll"))
			print("INFO: SteamworksPy loaded for Windows")
			Steam.loaded = True
		# Unrecognized platform, warn user, do not load Steam API
		else:
			print("ERROR: SteamworksPy failed to load (unsupported platform!)")
			Steam.warn = True
			return
		# Set restype for initialization
		Steam.cdll.IsSteamRunning.restype = c_bool
		# Check that Steam is running
		if Steam.cdll.IsSteamRunning():
			print("INFO: Steam is running")
		else:
			print("ERROR: Steam is not running")
		# Boot up the Steam API 
		if Steam.cdll.SteamInit() == 1:
			print("INFO: Steamworks initialized!")
		else:
			print("ERROR: Steamworks failed to initialize!")
		#----------------------------------------
		# Restypes and Argtypes
		#----------------------------------------
		# Set restype for Apps functions
		Steam.cdll.HasOtherApp.restype = bool
		Steam.cdll.GetDlcCount.restype = int
		Steam.cdll.IsDlcInstalled.restype = bool
		Steam.cdll.RequestAppProofOfPurchaseKey.restype = c_char_p
		Steam.cdll.IsAppInstalled.restype = bool
		Steam.cdll.GetCurrentGameLanguage.restype = c_char_p
		# Set restype for Friends functions
		Steam.cdll.GetFriendCount.restype = int
		Steam.cdll.GetFriendByIndex.restype = c_uint64
		Steam.cdll.GetPersonaName.restype = c_char_p
		Steam.cdll.GetPersonaState.restype = int
		Steam.cdll.GetFriendPersonaName.restype = c_char_p
		Steam.cdll.GetFriendPersonaName.argtypes = [c_uint64]
		Steam.cdll.SetGameInfo.restype = None
		Steam.cdll.ClearGameInfo.restype = None
		Steam.cdll.InviteFriend.restype = None
		Steam.cdll.SetPlayedWith.restype = None
#		Steam.cdll.GetRecentPlayers.restype = None
#		Steam.cdll.GetFriendAvatar.restype = None
#		Steam.cdll.DrawAvatar.restype = None
		Steam.cdll.ActivateGameOverlay.restype = None
		Steam.cdll.ActivateGameOverlay.argtypes = [c_char_p]
		Steam.cdll.ActivateGameOverlayToUser.restype = None
		Steam.cdll.ActivateGameOverlayToUser.argtypes = [c_char_p, c_uint32]
		Steam.cdll.ActivateGameOverlayToWebPage.restype = None
		Steam.cdll.ActivateGameOverlayToWebPage.argtypes = [c_char_p]
		Steam.cdll.ActivateGameOverlayToStore.restype = None
		Steam.cdll.ActivateGameOverlayToStore.argtypes = [c_uint32]
		Steam.cdll.ActivateGameOverlayInviteDialog.restype = None
		Steam.cdll.ActivateGameOverlayInviteDialog.argtypes = [c_uint64]
		# Set restype for Matchmaking
		Steam.cdll.CreateLobby.restype = None
		Steam.cdll.CreateLobby.argtypes = [c_uint64, c_uint64]
		Steam.cdll.JoinLobby.restype = None
		Steam.cdll.JoinLobby.argtypes = [c_uint64]
		Steam.cdll.LeaveLobby.restype = None
		Steam.cdll.LeaveLobby.argtypes = [c_uint64]
		Steam.cdll.InviteUserToLobby.restype = bool
		Steam.cdll.InviteUserToLobby.argtypes = [c_uint64, c_uint64]
		# Set restype for Music functions
		Steam.cdll.MusicIsEnabled.restype = bool
		Steam.cdll.MusicIsPlaying.restype = bool
		Steam.cdll.MusicGetVolume.restype = c_float
		Steam.cdll.MusicPause.restype = bool
		Steam.cdll.MusicPlay.restype = bool
		Steam.cdll.MusicPlayNext.restype = bool
		Steam.cdll.MusicPlayPrev.restype = bool
		Steam.cdll.MusicSetVolume.restype = c_float
		# Set restype for Screenshot functions
		Steam.cdll.TriggerScreenshot.restype = None
		# Set restype for User functions		
		Steam.cdll.GetSteamID.restype = c_uint64
		Steam.cdll.GetPlayerSteamLevel.restype = int
		Steam.cdll.GetUserDataFolder.restype = c_char_p
		# Set restype for User Statistic functions
		Steam.cdll.GetAchievement.restype = bool
		Steam.cdll.GetStatInt.restype = int
		Steam.cdll.GetStatFloat.restype = c_float
		Steam.cdll.ResetAllStats.restype = bool
		Steam.cdll.RequestCurrentStats.restype = bool
		Steam.cdll.SetAchievement.restype = bool
		Steam.cdll.SetStatInt.restype = bool
		Steam.cdll.SetStatFloat.restype = bool
		Steam.cdll.StoreStats.restype = bool
		Steam.cdll.ClearAchievement.restype = bool
#		Steam.cdll.FindLeaderboard.restype = None
#		Steam.cdll.FindLeaderboard.argtypes = [c_char_p]
#		Steam.cdll.GetLeaderboardName.restype = c_char_p
#		Steam.cdll.GetLeaderboardEntryCount.restype = int
#		Steam.cdll.DownloadLeaderboardEntries.restype = None
#		Steam.cdll.DownloadLeaderboardEntries.argtypes = [int, int, int]
#		Steam.cdll.DownloadLeaderboardEntriesForUsers.restype = None
#		Steam.cdll.UploadLeaderboardScore.restype = None
#		Steam.cdll.UploadLeaderboardScore.argtypes = [int, bool]
#		Steam.cdll.GetDownloadLeaderboardEntry.restype = None
#		Steam.cdll.UpdateLeaderboardHandle.restype = None
#		Steam.cdll.GetLeadboardHandle.restype = c_uint64
#		Steam.cdll.GetLeaderboardEntries.restype = None
		# Set restype for Utilities functions
		Steam.cdll.GetCurrentBatteryPower.restype = int
		Steam.cdll.GetIPCountry.restype = c_char_p
		Steam.cdll.GetSecondsSinceAppActive.restype = int
		Steam.cdll.GetSecondsSinceComputerActive.restype = int
		Steam.cdll.GetServerRealTime.restype = int
		Steam.cdll.IsOverlayEnabled.restype = bool
		Steam.cdll.IsSteamRunningInVR.restype = bool
		Steam.cdll.GetSteamUILanguage.restype = c_char_p
		Steam.cdll.GetAppID.restype = int
		Steam.cdll.SetOverlayNotificationPosition.restype = None
		# Set argtypes and restype for Workshop functions
		Steam.cdll.Workshop_StartItemUpdate.restype = c_uint64
		Steam.cdll.Workshop_SetItemTitle.restype = bool
		Steam.cdll.Workshop_SetItemTitle.argtypes = [c_uint64, c_char_p]
		Steam.cdll.Workshop_SetItemDescription.restype = bool
		Steam.cdll.Workshop_SetItemDescription.argtypes = [c_uint64, c_char_p]
		Steam.cdll.Workshop_SetItemUpdateLanguage.restype = bool
		Steam.cdll.Workshop_SetItemMetadata.restype = bool
		Steam.cdll.Workshop_SetItemVisibility.restype = bool
		Steam.cdll.Workshop_SetItemTags.restype = bool
		Steam.cdll.Workshop_SetItemContent.restype = bool
		Steam.cdll.Workshop_SetItemContent.argtypes = [c_uint64, c_char_p]
		Steam.cdll.Workshop_SetItemPreview.restype = bool
		Steam.cdll.Workshop_SetItemPreview.argtypes = [c_uint64, c_char_p]
		Steam.cdll.Workshop_SubmitItemUpdate.argtypes = [c_uint64, c_char_p]
		Steam.cdll.Workshop_GetNumSubscribedItems.restype = c_uint32
		Steam.cdll.Workshop_GetSubscribedItems.restype = c_uint32
		Steam.cdll.Workshop_GetSubscribedItems.argtypes = [POINTER(c_uint64), c_uint32]
		Steam.cdll.Workshop_GetItemState.restype = c_uint32
		Steam.cdll.Workshop_GetItemState.argtypes = [c_uint64]
		Steam.cdll.Workshop_GetItemInstallInfo.restype = bool
		Steam.cdll.Workshop_GetItemInstallInfo.argtypes = [c_uint64, POINTER(c_uint64), c_char_p, c_uint32,  POINTER(c_uint32)]
		Steam.cdll.Workshop_GetItemDownloadInfo.restype = bool
		Steam.cdll.Workshop_GetItemDownloadInfo.argtypes = [c_uint64, POINTER(c_uint64), POINTER(c_uint64)]
	# Is Steam loaded
	@staticmethod
	def isSteamLoaded():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return True
	# Yeah
	@staticmethod
	def Call(method):
		if Steam.isSteamLoaded():
			return method()
		else:
			return False
	# Running callbacks
	@staticmethod
	def RunCallbacks():
		if Steam.isSteamLoaded():
			Steam.cdll.RunCallbacks()
			return True
		else:
			return False
#------------------------------------------------
# Class for Steam Apps
#------------------------------------------------
class SteamApps:
	# Check if the user has a given application/game
	@staticmethod
	def HasOtherApp(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.HasOtherApp(appID)
		else:
			return False
	# Get the number of DLC the user owns for a parent application/game
	@staticmethod
	def GetDlcCount():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetDlcCount()
		else:
			return 0
	# Check give the given DLC is installed, returns true/false
	@staticmethod
	def IsDlcInstalled(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.IsDlcInstalled(appID)
		else:
			return False
	# Returns purchase key for given application/game
	@staticmethod
	def RequestAppProofOfPurchaseKey(value):
		if Steam.isSteamLoaded():
			return Steam.cdll.RequestAppProofOfPurchaseKey(value)
		else:
			return "None"
	# Check if given application/game is installed, not necessarily owned
	@staticmethod
	def IsAppInstalled(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.IsAppInstalled(appID)
		else:
			return False
	# Get the user's game language
	@staticmethod
	def GetCurrentGameLanguage():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetCurrentGameLanguage()
		else:
			return "None"
#------------------------------------------------
# Class for Steam Friends
#------------------------------------------------
class SteamFriends:
	# Get number of friends user has
	@staticmethod
	def GetFriendCount(flag=FriendFlags['All']):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFriendCount(flag)
		else:
			return 0
	# Get a friend by index
	@staticmethod
	def GetFriendByIndex(friendInt, flag=FriendFlags['All']):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFriendByIndex(friendInt, flag)
		else:
			return 0
	# Get the user's Steam username
	@staticmethod
	def GetPlayerName():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetPersonaName()
		else:
			return ""
	# Get the user's state on Steam
	@staticmethod
	def GetPlayerState():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetPersonaState()
		else:
			return False
	# Get given friend's Steam username
	@staticmethod
	def GetFriendPersonaName(steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFriendPersonaName(steamID)
		else:
			return ""
	# Set the game information in Steam; used in 'View Game Info'
	@staticmethod
	def SetGameInfo(serverKey, serverValue):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetGameInfo(serverKey, serverValue)
		else:
			return
	# Clear the game information in Steam; used in 'View Game Info'
	@staticmethod
	def ClearGameInfo():
		if Steam.isSteamLoaded():
			return Steam.cdll.ClearGameInfo()
		else:
			return
	# Invite friend to current game/lobby
	@staticmethod
	def InviteFriend(steamID, connection):
		if Steam.isSteamLoaded():
			return Steam.cdll.InviteFriend(steamID, connection)	
		else:
			return
	# Set player as 'Played With' for game
	@staticmethod
	def SetPlayedWith(steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetPlayedWith(steamID)
		else:
			return
	# Activates the overlay with optional dialog to open the following: "Friends", "Community", "Players", "Settings", "OfficialGameGroup", "Stats", "Achievements", "LobbyInvite"
	@staticmethod
	def ActivateGameOverlay(dialog=''):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlay(dialog.encode())
		else:
			return
	# Activates the overlay to the following: "steamid", "chat", "jointrade", "stats", "achievements", "friendadd", "friendremove", "friendrequestaccept", "friendrequestignore"
	@staticmethod
	def ActivateGameOverlayToUser(url, steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlayToWebPage(url.encode(), steamID)
		else:
			return
	# Activates the overlay with specified web address
	@staticmethod
	def ActivateGameOverlayToWebPage(url):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlayToWebPage(url.encode())
		else:
			return
	# Activates the overlay with the application/game Steam store page
	@staticmethod
	def ActivateGameOverlayToStore(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlayToWebPage(appID)
		else:
			return
	# Activates game overlay to open the invite dialog. Invitations will be sent for the provided lobby
	@staticmethod
	def ActivateGameOverlayInviteDialog(steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlayToWebPage(steamID)
		else:
			return
#------------------------------------------------
# Class for Steam Matchmaking
#------------------------------------------------ 
class SteamMatchmaking:
	# Create a lobby on the Steam servers, if private the lobby will not be returned by any RequestLobbyList() call
	@staticmethod
	def CreateLobby(lobbyType, maxMembers):
		if Steam.isSteamLoaded():
			return Steam.cdll.CreateLobby(lobbyType, maxMembers)
		else:
			return
	# Join an existing lobby
	@staticmethod
	def JoinLobby(lobbyID):
		if Steam.isSteamLoaded():
			return Steam.cdll.JoinLobby(lobbyID)
		else:
			return
	# Leave a lobby, this will take effect immediately on the client side, other users will be notified by LobbyChatUpdate_t callback
	@staticmethod
	def LeaveLobby(lobbyID):
		if Steam.isSteamLoaded():
			return Steam.cdll.LeaveLobby(lobbyID)
		else:
			return
	# Invite another user to the lobby, the target user will receive a LobbyInvite_t callback, will return true if the invite is successfully sent, whether or not the target responds
	@staticmethod
	def InviteUserToLobby(lobbyID, steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.InviteUserToLobby(lobbyID, steamID)
		else:
			return
#------------------------------------------------
# Class for Steam Music
#------------------------------------------------
class SteamMusic:
	# Is Steam music enabled
	@staticmethod
	def MusicIsEnabled():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicIsEnabled()
		else:
			return False
	# Is Steam music playing something
	@staticmethod
	def MusicIsPlaying():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicIsPlaying()
		else:
			return False
	# Get the volume level of the music
	@staticmethod
	def MusicGetVolume():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicGetVolume()
		else:
			return 0
	# Pause whatever Steam music is playing
	@staticmethod
	def MusicPause():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicPause()
		else:
			return False
	# Play current track/album
	@staticmethod
	def MusicPlay():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicPlay()
		else:
			return False
	# Play next track/album
	@staticmethod
	def MusicPlayNext():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicPlayNext()
		else:
			return False
	# Play previous track/album
	@staticmethod
	def MusicPlayPrev():
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicPlayPrev()
		else:
			return False
	# Set the volume of Steam music
	@staticmethod
	def MusicSetVolume(value):
		if Steam.isSteamLoaded():
			return Steam.cdll.MusicSetVolume(value)
		else:
			return False
#------------------------------------------------
# Class for Steam Screenshots
#------------------------------------------------
class SteamScreenshots:
	# Causes Steam overlay to take a screenshot
	@staticmethod
	def TriggerScreenshot():
		if Steam.isSteamLoaded():
			return Steam.cdll.TriggerScreenshot()
		else:
			return
#------------------------------------------------
# Class for Steam Users
#------------------------------------------------
class SteamUser:
	# Get user's Steam ID
	@staticmethod
	def GetPlayerID():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSteamID()
		else:
			return 0
	# Get the user's Steam level
	@staticmethod
	def GetPlayerSteamLevel():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetPlayerSteamLevel()
		else:
			return 0
	# Get the user's Steam installation path
	@staticmethod
	def GetUserDataFolder():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetUserDataFolder()
		else:
			return ""
#------------------------------------------------
# Class for Steam User Statistics
#------------------------------------------------
class SteamUserStats:
	# Return true/false if use has given achievement
	@staticmethod
	def GetAchievement(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetAchievement(name)
		else:
			return ""
	# Get the value of a float statistic
	@staticmethod
	def GetStatFloat(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetStatFloat(name)
		else:
			return 0
	# Get the value of an integer statistic
	@staticmethod
	def GetStatInt(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetStatInt(name)
		else:
			return 0
	# Reset all Steam statistics; optional to reset achievements
	@staticmethod
	def ResetAllStats(achievesToo):
		if Steam.isSteamLoaded():
			return Steam.cdll.ResetAllStats(achievesToo)
		else:
			return False
	# Request all statistics and achievements from Steam servers
	@staticmethod
	def RequestCurrentStats():
		if Steam.isSteamLoaded():
			return Steam.cdll.RequestCurrentStats()
		else:
			return False
	# Set a given achievement
	@staticmethod
	def SetAchievement(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetAchievement(name)
		else:
			return False
	# Set a statistic
	@staticmethod
	def SetStat(name, value):
		if Steam.isSteamLoaded():
			if isinstance(value, float):
				return Steam.cdll.SetStatFloat(name, value)
			elif isinstance(value, int):
				return Steam.cdll.SetStatInt(name, value)
			else:
				raise Exception("SteamUserStats: SetStat value can be only int or float.")
	# Store all statistics, and achievements, on Steam servers; must be called to "pop" achievements
	@staticmethod
	def StoreStats():
		if Steam.isSteamLoaded():
			return Steam.cdll.StoreStats()
		else:
			return False
	# Clears a given achievement
	@staticmethod
	def ClearAchievement(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.ClearAchievement(name)
		else:
			return False
#------------------------------------------------
# Class for Steam Utilities
#------------------------------------------------
class SteamUtilities:
	# Get the amount of battery power, clearly for laptops
	@staticmethod
	def GetCurrentBatteryPower():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetCurrentBatteryPower()
		else:
			return 0
	# Get the user's country by IP
	@staticmethod
	def GetIPCountry():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetIPCountry()
		else:
			return "None"
	# Returns seconds since application/game was started
	@staticmethod
	def GetSecondsSinceAppActive():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSecondsSinceAppActive()
		else:
			return 0
	# Return seconds since computer was started
	@staticmethod
	def GetSecondsSinceComputerActive():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSecondsSinceComputerActive()
		else:
			return 0
	# Get the actual time
	@staticmethod
	def GetServerRealTime():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetServerRealTime()
		else:
			return 0
	# Returns true/false if Steam overlay is enabled
	@staticmethod
	def IsOverlayEnabled():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsOverlayEnabled()
		else:
			return False
	# Is Steam running in VR?
	@staticmethod
	def IsSteamRunningInVR():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsSteamRunningInVR()
		else:
			return False
	# Get the Steam user interface language
	@staticmethod
	def GetSteamUILanguage():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSteamUILanguage()
		else:
			return "None"
	# Get the Steam ID of the running application/game
	@staticmethod
	def GetAppID():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetAppID()
		else:
			return 0
	# Set the position where overlay shows notifications
	@staticmethod
	def SetOverlayNotificationPosition(pos):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetOverlayNotificationPosition(pos)
		else:
			return False
#------------------------------------------------
# Class for Steam Workshop
#------------------------------------------------
class SteamWorkshop:
	# A class that describes Steam's CreateItemResult_t C struct
	class CreateItemResult_t(Structure):
		_fields_ = [
			("result", c_int),
			("publishedFileId", c_uint64),
			("userNeedsToAcceptWorkshopLegalAgreement", c_bool)
		]
	# A class that describes Steam's SubmitItemUpdateResult_t C struct
	class SubmitItemUpdateResult_t(Structure):
		_fields_ = [
			("result", c_int),
			("userNeedsToAcceptWorkshopLegalAgreement", c_bool)
		]
	# A class that describes Steam's ItemInstalled_t C struct
	class ItemInstalled_t(Structure):
		_fields_ = [
			("appId", c_uint32),
			("publishedFileId", c_uint64)
		]
	# We want to keep callbacks in the class scope, so that they don't get
	# garbage collected while we still need them.
	ITEM_CREATED_CALLBACK_TYPE = CFUNCTYPE(None, CreateItemResult_t)
	itemCreatedCallback = None

	ITEM_UPDATED_CALLBACK_TYPE = CFUNCTYPE(None, SubmitItemUpdateResult_t)
	itemUpdatedCallback = None

	ITEM_INSTALLED_CALLBACK_TYPE = CFUNCTYPE(None, ItemInstalled_t)
	itemInstalledCallback = None
	#
	@classmethod
	def SetItemCreatedCallback(cls, callback):
		if Steam.isSteamLoaded():
			cls.itemCreatedCallback = cls.ITEM_CREATED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemCreatedCallback(cls.itemCreatedCallback)
		else:
			return False
	#
	@classmethod
	def SetItemUpdatedCallback(cls, callback):
		if Steam.isSteamLoaded():
			cls.itemUpdatedCallback = cls.ITEM_UPDATED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemUpdatedCallback(cls.itemUpdatedCallback)
		else:
			return False
	#
	@classmethod
	def SetItemInstalledCallback(cls, callback):
		if Steam.isSteamLoaded():
			cls.itemInstalledCallback = cls.ITEM_INSTALLED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemInstalledCallback(cls.itemInstalledCallback)
		else:
			return False
	#
	@classmethod
	def ClearItemInstalledCallback(cls, callback):
		if Steam.isSteamLoaded():
			itemInstalledCallback = None
			Steam.cdll.Workshop_ClearItemInstalledCallback()
	# Create a UGC (Workshop) item
	#
	# Arguments:
	# appId -- The app ID of the game on Steam. 
	# Do not use the creation tool app ID if they are separate.
	#
	# filetype -- Can be a community file type or microtransactions.
	# Use predefined `WorkshopFileType` values.
	#
	# callback -- The function to call once the item creation is finished.
	@staticmethod
	def CreateItem(appId, filetype, callback = None):
		if Steam.isSteamLoaded():
			if callback != None:
				SteamWorkshop.SetItemCreatedCallback(callback)

			Steam.cdll.Workshop_CreateItem(appId, filetype)
			return True
		else:
			return False
	# Start the item update process and receive an update handle.
	#
	# Arguments:
	# appId -- The app ID of the game on Steam. 
	# Do not use the creation tool app ID if they are separate
	# publishedFileId -- The ID of the Workshop file you are updating
	# 
	# Return value:
	# If sucessful: update handle - an ID of the current update transaction
	# Otherwise: False
	@staticmethod
	def StartItemUpdate(appId, publishedFileId):
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_StartItemUpdate(appId, c_uint64(publishedFileId))
		else:
			return False
	# Set the title of a Workshop item
	#
	# Arguments:
	# 
	# updateHandle -- the handle returned by 'StartItemUpdate'
	# title -- the desired title of the item.
	# 
	# Return value:
	# True on succes,
	# False otherwise.
	@staticmethod
	def SetItemTitle(updateHandle, title):
		if Steam.isSteamLoaded():
			if len(title) > 128:
				print("ERROR: Your title is longer than 128 characters.")
				return False

			return Steam.cdll.Workshop_SetItemTitle(updateHandle, title.encode())
		else:
			return False
	# Set the description of a Workshop item
	#
	# Arguments:
	# updateHandle -- the handle returned by 'StartItemUpdate'
	# description -- the desired description of the item.
	#
	# Return value:
	# True on succes,
	# False otherwise.
	@staticmethod
	def SetItemDescription(updateHandle, description):
		if Steam.isSteamLoaded():
			if len(description) > 8000:
				print("ERROR: Your description is longer than 8000 characters.")
				return False

			return Steam.cdll.Workshop_SetItemDescription(updateHandle, description.encode())
		else:
			return False
	# Set the directory containing the content you wish to upload to Workshop.
	#
	# Arguments:
	# updateHandle -- the handle returned by 'StartItemUpdate'
	# contentDirectory -- path to the directory containing the content of the workshop item.
	#
	# Return value:
	# True on succes,
	# False otherwise.
	@staticmethod
	def SetItemContent(updateHandle, contentDirectory):
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_SetItemContent(updateHandle, contentDirectory.encode())
		else:
			return False
	# Set the preview image of the Workshop item.
	#
	# Arguments:
	# updateHandle -- the handle returned by 'StartItemUpdate'
	# previewImage -- path to the preview image file.
	#
	# Return value:
	# True on succes,
	# False otherwise.
	@staticmethod
	def SetItemPreview(updateHandle, previewImage):
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_SetItemPreview(updateHandle, previewImage.encode())
		else:
			return False
	# Submit the item update with the given handle to Steam.
	#
	# Arguments:
	# updateHandle -- the handle returned by 'StartItemUpdate'
	# changeNote -- a string containing change notes for the current update.
	@staticmethod
	def SubmitItemUpdate(updateHandle, changeNote, callback = None):
		if Steam.isSteamLoaded():
			if callback != None:
				SteamWorkshop.SetItemUpdatedCallback(callback)

			return Steam.cdll.Workshop_SubmitItemUpdate(updateHandle, changeNote.encode())
		else:
			return False
	# Get the progress of an item update request.
	#
	# Argument:
	# updateHandle -- the handle returned by 'StartItemUpdate'
	#
	# Return Value:
	# On success: An object with the following attributes
	# -- 'itemUpdateStatus - a `WorkshopItemUpdateStatus` value describing the update status of the item
	# -- 'bytesProcessed' - amount of bytes processed
	# -- 'bytesTotal' - total amount of bytes to be processed
	# -- 'progress' - a value ranging from 0 to 1 representing update progress
	# Otherwise: False
	@staticmethod
	def GetItemUpdateProgress(updateHandle):
		if Steam.isSteamLoaded():
			pBytesProcessed = pointer(c_uint64)
			pBytesTotal = pointer(c_uint64)

			itemUpdateStatus = Workshop_GetItemUpdateProgress(updateHandle, pBytesProcessed, pBytesTotal)
			# Unlike for GetItemDownloadInfo, pBytesTotal should always be set here
			progress = pBytesProcessed.contents.value / pBytesTotal.contents.value

			itemUpdateInfo = {
				'itemUpdateStatus' : itemUpdateStatus,
				'bytesProcessed' : pBytesProcessed.contents.value,
				'bytesTotal' : pBytesTotal.contents.value,
				'progress' : progress
			}

			return itemUpdateInfo
		else:
			return False
	# Get the total number of items the user is subscribed to for this game or application.
	#
	# Return value:
	# On success: The number of subscribed items,
	# Otherwise: False.
	@staticmethod
	def GetNumSubscribedItems():
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_GetNumSubscribedItems()
		else:
			return False
	# Get a list of published file IDs that the user is subscribed to
	#
	# Arguments:
	# maxEntries -- the maximum number of entries to fetch. If omitted
	# the function will try to fetch as much items as the user is 
	# subscribed to.
	#
	# Return Value:
	# On success: A list of published file IDs that the user is subscribed to.
	# Otherwise: False.
	@staticmethod
	def GetSubscribedItems(maxEntries=-1):
		if Steam.isSteamLoaded():
			if maxEntries < 0:
				maxEntries = SteamWorkshop.GetNumSubscribedItems()
			# Published file IDs are stored as uint64 values
			PublishedFileIdsArrayCType = c_uint64 * maxEntries
			pvecPublishedFileIds = PublishedFileIdsArrayCType()

			# TODO: We might need to add an exception check here to catch any errors while
			# writing to the 'pvecPublishedFileIds' array.
			numItems = Steam.cdll.Workshop_GetSubscribedItems(pvecPublishedFileIds, maxEntries)
			# According to steam's example, it is possible for numItems to be greater than maxEntries
			# so we crop.
			if numItems > maxEntries:
				numItems = maxEntries

			publishedFileIdsList = [pvecPublishedFileIds[i] for i in range(numItems)]
			return publishedFileIdsList
		else:
			return False
	# Get the current state of a workshop item.
	#
	# Arguments:
	# publishedFileId -- the id of the item whose state to check
	#
	# Return Value:
	# On success: A `WorkshopItemState` value describing the item state.
	# Otherwise: False
	@staticmethod
	def GetItemState(publishedFileId):
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_GetItemState(publishedFileId)
		else:
			return False
	# Get info about an installed item
	#
	# Arguments:
	# publishedFileId -- the id of the item to look up,
	# maxFolderPathLength -- maximum length of the folder path in characters.
	#
	# Return Value:
	# If the item is installed: an object with the following attributes
	# -- 'sizeOnDisk'
	# -- 'folder'
	# -- 'timestamp'
	#
	# If the item is not installed, or the method fails it returns: False
	@staticmethod
	def GetItemInstallInfo(publishedFileId, maxFolderPathLength=1024):
		if Steam.isSteamLoaded():
			pSizeOnDisk = pointer(c_uint64(0))
			pTimestamp = pointer(c_uint32(0))
			pFolder = create_string_buffer(maxFolderPathLength)

			isInstalled = Steam.cdll.Workshop_GetItemInstallInfo(publishedFileId, pSizeOnDisk, pFolder, maxFolderPathLength, pTimestamp)

			if isInstalled:
				itemInfo = {
					'sizeOnDisk' : pSizeOnDisk.contents.value,
					'folder' : pFolder.value.decode(),
					'timestamp' : pTimestamp.contents.value
				}

				return itemInfo

		return False
	# Get download info for a subscribed item
	#
	# Arguments:
	# publishedFileId -- the id of the item whose download info to look up
	#
	# Return Value:
	# If download information is available returns an object with
	# the following attributes
	# -- 'bytesDownloaded'- the amount of downloaded bytes
	# -- 'bytesTotal' - the total amounts of bytes an item has
	# -- 'progress' - a value ranging from 0 to 1 representing download progress
	#
	# If download information or steamworks or not available, 
	# returns False
	@staticmethod
	def GetItemDownloadInfo(publishedFileId):
		if Steam.isSteamLoaded():
			pBytesDownloaded = pointer(c_uint64(0))
			pBytesTotal = pointer(c_uint64(0))
			# NOTE: pBytesTotal will only be valid after the download has started.
			downloadInfoAvailable = Steam.cdll.Workshop_GetItemDownloadInfo(publishedFileId, pBytesDownloaded, pBytesTotal)
			if downloadInfoAvailable:
				bytesDownloaded = pBytesDownloaded.contents.value
				bytesTotal = pBytesTotal.contents.value
				progress = 0
				if bytesTotal > 0:
					progress = bytesDownloaded / bytesTotal
				downloadInfo = {
					'bytesDownloaded' : bytesDownloaded,
					'bytesTotal' : bytesTotal,
					'progress' : progress
				}
				return downloadInfo
			return False
		else:
			return False
