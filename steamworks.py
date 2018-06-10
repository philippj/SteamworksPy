#=========================================================================
# Steamworks For Python
#=========================================================================
from ctypes import *
import sys, os
#-------------------------------------------------------------------------
# User Status
#-------------------------------------------------------------------------
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
#-------------------------------------------------------------------------
# Workshop File Types
#-------------------------------------------------------------------------
WorkshopFileType = {
	'Community': 0x00,			# normal Workshop item that can be subscribed to
	'Microtransaction': 0x01,	# Workshop item that is meant to be voted on for the purpose of selling in-game

	# NOTE: There are more workshop file types defined "in isteamremotestorage.h",
	# but we do not need them for now.
}
#-------------------------------------------------------------------------
# Workshop Item States
#-------------------------------------------------------------------------
WorkshopItemState = {
	"ItemStateNone":			0,	# item not tracked on client
	"ItemStateSubscribed":		1,	# current user is subscribed to this item. Not just cached.
	"ItemStateLegacyItem":		2,	# item was created with ISteamRemoteStorage
	"ItemStateInstalled":		4,	# item is installed and usable (but maybe out of date)
	"ItemStateNeedsUpdate":		8,	# items needs an update. Either because it's not installed yet or creator updated content
	"ItemStateDownloading":		16,	# item update is currently downloading
	"ItemStateDownloadPending":	32,	# DownloadItem() was called for this item, content isn't available until DownloadItemResult_t is fired
}
#-------------------------------------------------------------------------
# Main Steam Class, obviously
#-------------------------------------------------------------------------
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
		#-----------------------------------------------------------------
		# Restypes and Argtypes
		#-----------------------------------------------------------------
		# Set restype for Apps functions #################################
		Steam.cdll.HasOtherApp.restype = bool
		Steam.cdll.GetDLCCount.restype = int
		Steam.cdll.IsDlcInstalled.restype = bool
		Steam.cdll.IsAppInstalled.restype = bool
		Steam.cdll.GetCurrentGameLanguage.restype = c_char_p
		Steam.cdll.IsVACBanned.restype = bool
		Steam.cdll.GetEarliestPurchaseUnixTime.restype = int
		Steam.cdll.IsSubscribedFromFreeWeekend.restype = bool
		Steam.cdll.InstallDLC.restype = None
		Steam.cdll.UninstallDLC.restype = None
		Steam.cdll.IsSubscribed.restype = bool
		Steam.cdll.IsLowViolence.restype = bool
		Steam.cdll.IsCybercafe.restype = bool
		Steam.cdll.IsSubscribedApp.restype = bool
		Steam.cdll.GetAppBuildId.restype = int
		# Set restype for Friends functions ##############################
		Steam.cdll.GetFriendCount.restype = int
		Steam.cdll.GetPersonaName.restype = c_char_p
		Steam.cdll.GetFriendPersonaName.restype = c_char_p
		Steam.cdll.SetGameInfo.restype = None
		Steam.cdll.ClearGameInfo.restype = None
		Steam.cdll.InviteFriend.restype = None
		Steam.cdll.SetPlayedWith.restype = None
		Steam.cdll.GetFriendAvatar.restype = None
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
		# Set restype for Matchmaking ####################################
		Steam.cdll.CreateLobby.restype = None
		Steam.cdll.CreateLobby.argtypes = [c_uint64, c_uint64]
		Steam.cdll.JoinLobby.restype = None
		Steam.cdll.JoinLobby.argtypes = [c_uint64]
		Steam.cdll.LeaveLobby.restype = None
		Steam.cdll.LeaveLobby.argtypes = [c_uint64]
		Steam.cdll.InviteUserToLobby.restype = bool
		Steam.cdll.InviteUserToLobby.argtypes = [c_uint64, c_uint64]
		# Set restype for Music functions ################################
		Steam.cdll.MusicIsEnabled.restype = bool
		Steam.cdll.MusicIsPlaying.restype = bool
		Steam.cdll.MusicGetVolume.restype = c_float
		Steam.cdll.MusicPause.restype = bool
		Steam.cdll.MusicPlay.restype = bool
		Steam.cdll.MusicPlayNext.restype = bool
		Steam.cdll.MusicPlayPrev.restype = bool
		Steam.cdll.MusicSetVolume.restype = c_float
		# Set restype for Remote Storage functions #######################
#		Steam.cdll.FileWrite.restype = bool
		Steam.cdll.FileForget.restype = bool
		Steam.cdll.FileDelete.restype = bool
		Steam.cdll.FileExists.restype = bool
		Steam.cdll.FilePersisted.restype = bool
		Steam.cdll.GetFileSize.restype = int
		Steam.cdll.GetFileTimestamp.restype = int
		Steam.cdll.GetFileCount.restype = int
		Steam.cdll.IsCloudEnabledForAccount.restype = bool
		Steam.cdll.IsCloudEnabledForApp.restype = bool
		Steam.cdll.SetCloudEnabledForApp.restype = None
		Steam.cdll.GetSyncPlatforms.restype = int
		# Set restype for Screenshot functions ###########################
		Steam.cdll.HookScreenshots.restype = None
		Steam.cdll.IsScreenshotsHooked.restype = bool
		Steam.cdll.TriggerScreenshot.restype = None
		# Set restype for User functions #################################
		Steam.cdll.EndAuthSession.restype = None
		Steam.cdll.GetSteamID.restype = int
		Steam.cdll.LoggedOn.restype = bool
		Steam.cdll.GetPlayerSteamLevel.restype = int
#		Steam.cdll.GetUserDataFolder.restype = c_char_p
		Steam.cdll.GetGameBadgeLevel.restype = int
		# Set restype for User Statistic functions #######################
		Steam.cdll.GetAchievement.restype = bool
		Steam.cdll.GetNumAchievements.restype = int
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
		Steam.cdll.GetLeadboardHandle.restype = c_uint64
		Steam.cdll.GetLeaderboardEntries.restype = None
		Steam.cdll.GetAchievementAndUnlockTime.restype = bool
		Steam.cdll.IndicateAchievementProgress.restype = bool
		# Set restype for Utilities functions ############################
		Steam.cdll.GetCurrentBatteryPower.restype = int
		Steam.cdll.GetIPCountry.restype = c_char_p
		Steam.cdll.GetSecondsSinceAppActive.restype = int
		Steam.cdll.GetServerRealTime.restype = int
		Steam.cdll.IsOverlayEnabled.restype = bool
		Steam.cdll.IsSteamRunningInVR.restype = bool
		Steam.cdll.IsSteamInBigPictureMode.restype = bool
		Steam.cdll.StartVRDashboard.restype = None
		Steam.cdll.GetSteamUILanguage.restype = c_char_p
		Steam.cdll.GetAppID.restype = int
		Steam.cdll.SetOverlayNotificationPosition.restype = None
		# Set argtypes and restype for Workshop functions ################
		Steam.cdll.DownloadItem.restype = bool
		Steam.cdll.DownloadItem.argtypes [int, bool]
		Steam.cdll.SuspendDownloads.restype = None
		Steam.cdll.StartItemUpdate.restype = c_uint64
		Steam.cdll.GetItemState.restype = int
		Steam.cdll.GetItemUpdateProgress.restype = int
		Steam.cdll.CreateItem.restype = None
		Steam.cdll.SetItemTitle.restype = bool
		Steam.cdll.SetItemTitle.argtypes = [c_uint64, c_char_p]
		Steam.cdll.SetItemDescription.restype = bool
		Steam.cdll.SetItemDescription.argtypes = [c_uint64, c_char_p]
		Steam.cdll.SetItemUpdateLanguage.restype = bool
		Steam.cdll.SetItemMetadata.restype = bool
		Steam.cdll.SetItemVisibility.restype = bool
		Steam.cdll.SetItemTags.restype = bool
		Steam.cdll.SetItemContent.restype = bool
		Steam.cdll.SetItemContent.argtypes = [c_uint64, c_char_p]
		Steam.cdll.SetItemPreview.restype = bool
		Steam.cdll.SetItemPreview.argtypes = [c_uint64, c_char_p]
		Steam.cdll.SubmitItemUpdate.restype = None
		Steam.cdll.SubmitItemUpdate.argtypes = [c_uint64, c_char_p]
		Steam.cdll.GetNumSubscribedItems.restype = c_uint32
		Steam.cdll.GetSubscribedItems.restype = c_uint32
		Steam.cdll.GetSubscribedItems.argtypes = [POINTER(c_uint64), c_uint32]
#		Steam.cdll.GetItemState.restype = c_uint32
#		Steam.cdll.GetItemState.argtypes = [c_uint64]
#		Steam.cdll.GetItemInstallInfo.restype = bool
#		Steam.cdll.GetItemInstallInfo.argtypes = [c_uint64, POINTER(c_uint64), c_char_p, c_uint32,  POINTER(c_uint32)]
#		Steam.cdll.GetItemDownloadInfo.restype = bool
#		Steam.cdll.GetItemDownloadInfo.argtypes = [c_uint64, POINTER(c_uint64), POINTER(c_uint64)]
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
	#---------------------------------------------------------------------
	# Definitions for Apps
	#---------------------------------------------------------------------
	# Check if the user has a given application/game
	@staticmethod
	def HasOtherApp(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.HasOtherApp(appID)
		else:
			return False
	# Get the number of DLC the user owns for a parent application/game
	@staticmethod
	def GetDLCCount():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetDLCCount()
		else:
			return 0
	# Check give the given DLC is installed, returns true/false
	@staticmethod
	def IsDlcInstalled(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.IsDlcInstalled(appID)
		else:
			return False
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
	# Does the user have a VAC ban for this game
	@staticmethod
	def IsVACBanned():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsVACBanned()
		else:
			return False
	# Returns the Unit time of the purchase of the app
	@staticmethod
	def GetEarliestPurchaseUnixTime(value):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetEarliestPurchaseUnixTime(value)
		else:
			return 0
	# Check if the user is subscribed to the current app
	@staticmethod
	def IsSubscribedFromFreeWeekend():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsSubscribedFromFreeWeekend()
		else:
			return False
	# Install control for optional DLC
	@staticmethod
	def InstallDLC(value):
		if Steam.isSteamLoaded():
			return Steam.cdll.InstallDLC(value)
		else:
			return
	# Uninstall control for optional DLC
	@staticmethod
	def UninstallDLC(value):
		if Steam.isSteamLoaded():
			return Steam.cdll.UninstallDLC(value)
		else:
			return
	# Is subscribed lacks notes
	@staticmethod
	def IsSubscribed():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsSubscribed()
		else:
			return False
	# Presumably if set to low violence
	@staticmethod
	def IsLowViolence():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsLowViolence()
		else:
			return False
	# Presumably if user is a cyber cafe
	@staticmethod
	def IsCybercafe():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsCybercafe()
		else:
			return False
	# Only used to check ownership of another game
	@staticmethod
	def IsSubscribedApp(appID):
		if Steam.isSteamLoaded():
			return Steam.cdll.IsSubscribedApp(appID)
		else:
			return False
	# Return the build ID for this app
	@staticmethod
	def GetAppBuildId:
		if Steam.isSteamLoaded():
			return Steam.cdll.GetAppBuildId()
		else:
			return 0
	#---------------------------------------------------------------------
	# Definitions for Friends
	#---------------------------------------------------------------------
	# Get number of friends user has
	@staticmethod
	def GetFriendCount(flag=FriendFlags['All']):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFriendCount(flag)
		else:
			return 0
	# Get the user's Steam username
	@staticmethod
	def GetPlayerName():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetPersonaName()
		else:
			return ""
	# Get given friend's Steam username
	@staticmethod
	def GetFriendName(steamID):
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
	#---------------------------------------------------------------------
	# Definitions for Matchmaking
	#---------------------------------------------------------------------
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
	#---------------------------------------------------------------------
	# Definitions for Music
	#---------------------------------------------------------------------
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
	#---------------------------------------------------------------------
	# Definitions for Remote Storage
	#---------------------------------------------------------------------
	# Delete file from remote storage but leave it on local disk to remain accessible
	@staticmethod
	def FileForget(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.FileForget(file)
		else:
			return False
	# Delete a given file in Steam Cloud
	@staticmethod
	def FileDelete(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.FileDelete(file)
		else:
			return False
	# Check if a givenfile exists in Steam Cloud
	@staticmethod
	def FileExists(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.FileExists(file)
		else:
			return False
	# Check if a given file is persisted in Steam Cloud
	@staticmethod
	def FilePersisted(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.FilePersisted(file)
		else:
			return False
	# Get the size of a given file
	@staticmethod
	def GetFileSize(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFileSize(file)
		else:
			return -1
	# Get the timestamp of when the file was uploaded/changed
	@staticmethod
	def GetFileTimestamp(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFileTimestamp(file)
		else:
			return -1
	# Gets the total number of local files synchronized by Steam Cloud
	@staticmethod
	def GetFileCount():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetFileCount()
		else:
			return 0
	# Is Steam Cloud enabled on the user's account?
	@staticmethod
	def IsCloudEnabledForAccount():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsCloudEnabledForAccount()
		else:
			return False
	# Is Steam Cloud enabled for this application?
	@staticmethod
	def IsCloudEnabledForApp():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsCloudEnabledForApp()
		else:
			return False
	# Set Steam Cloud enabled for this application
	@staticmethod
	def SetCloudEnabledForApp(enabled):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetCloudEnabledForApp(enabled)
		else:
			return
	# Obtains the platforms that the specified file will syncronize to
	@staticmethod
	def GetSyncPlatforms(file):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSyncPlatforms(file)
		else:
			return 0
	#---------------------------------------------------------------------
	# Definitions for Screenshots
	#---------------------------------------------------------------------
	# Toggles whether the overlay handles screenshots
	@staticmethod
	def HookScreenshots(hook):
		if Steam.isSteamLoaded():
			return Steam.cdll.HookScreenshots(hook)
		else:
			return
	# Checks if the app is hooking screenshots
	@staticmethod
	def IsScreenshotsHooked():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsScreenshotsHooked()
		else:
			return False
	# Causes Steam overlay to take a screenshot
	@staticmethod
	def TriggerScreenshot():
		if Steam.isSteamLoaded():
			return Steam.cdll.TriggerScreenshot()
		else:
			return
	#---------------------------------------------------------------------
	# Definitions for Users
	#---------------------------------------------------------------------
	# Ends an auth session
	@staticmethod
	def EndAuthSession(steamID):
		if Steam.isSteamLoaded():
			return Steam.cdll.EndAuthSession(steamID)
		else:
			return
	# Get user's Steam ID
	@staticmethod
	def GetSteamID():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetSteamID()
		else:
			return 0
	# Check, true/false, if user is logged into Steam currently
	@staticmethod
	def LoggedOn():
		if Steam.isSteamLoaded():
			return Steam.cdll.LoggedOn()
		else:
			return False
	# Get the user's Steam level
	@staticmethod
	def GetPlayerSteamLevel():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetPlayerSteamLevel()
		else:
			return 0
	# Get the user's Steam installation path
#	@staticmethod
#	def GetUserDataFolder():
#		if Steam.isSteamLoaded():
#			return Steam.cdll.GetUserDataFolder()
#		else:
#			return ""
	# Trading card badges data access, if you only have one set of cards, the series will be 1
	@staticmethod
	def GetGameBadgeLevel(series, foil):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetGameBadgeLevel(series, foil)
		else:
			return 0
	#---------------------------------------------------------------------
	# Definitions for User Statistics
	#---------------------------------------------------------------------
	# Return true/false if use has given achievement
	@staticmethod
	def GetAchievement(name):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetAchievement(name)
		else:
			return ""
	# Get the amount of players currently playing the current game
	@staticmethod
	def GetNumberOfCurrentPlayers():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetNumberOfCurrentPlayers()
		else:
			return
	# Get the number of achievements
	@staticmethod
	def GetNumAchievements():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetNumAchievements()
		else:
			return 0
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
	# Get the currently used leaderboard handle
	@staticmethod
	def GetLeadboardHandle():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetLeaderboardHandle()
		else:
			return 0
	# Get the currently used leaderboard entries
	@staticmethod
	def GetLeaderboardEntries():
		if Steam.isSteamLoaded():
			return Steam.cdll.GetLeaderboardEntries()
		else:
			return ""
	# Get the achievement status, and the time it was unlocked if unlocked
	@staticmethod
	def GetAchievementAndUnlockTime(name, achieved, unlockTime):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetAchievementAndUnlockTime(name, achieved, unlockTime)
		else:
			return 0
	# Achievement progress, triggers an AcheivementProgress callback, that is all
	@staticmethod
	def IndicateAchievementProgress(name, currentProgress, maxProgress):
		if Steam.isSteamLoaded():
			return Steam.cdll.IndicateAchievementProgress(name, currentProgress, maxProgress)
		else:
			return 0
	#---------------------------------------------------------------------
	# Definitions for Utilities
	#---------------------------------------------------------------------
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
	# Returns true if Steam & Steam Overlay in Big Picture Mode
	@staticmethod
	def IsSteamInBigPictureMode():
		if Steam.isSteamLoaded():
			return Steam.cdll.IsSteamInBigPictureMode()
		else:
			return False
	# Ask SteamUI to create and render its OpenVR dashboard
	@staticmethod
	def StartVRDashboard():
		if Steam.isSteamLoaded():
			return Steam.cdll.StartVRDashboard()
		else:
			return
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
	#---------------------------------------------------------------------
	# Defintions for Workshop
	#---------------------------------------------------------------------
	# Download new or update already installed item.
	@staticmethod
	def DownloadItem(fileID, priority):
		if Steam.isSteamLoaded():
			return Steam.cdll.DownloadItem(fileID, priority)
		else:
			return 0
	# "True" will suspend all workshop downloads until "false" is called or the game ends
	@staticmethod
	def SuspendDownloads(suspend):
		if Steam.isSteamLoaded():
			return Steam.cdll.SuspendDownloads(suspend)
		else:
			return
	# Create a UGC (Workshop) item
	@staticmethod
	def CreateItem(appID, filetype):
		if Steam.isSteamLoaded():
			Steam.cdll.CreateItem(appID, filetype)
			return True
		else:
			return False
	# Start the item update process and receive an update handle.
	@staticmethod
	def StartItemUpdate(appID, fileID):
		if Steam.isSteamLoaded():
			return Steam.cdll.StartItemUpdate(appId, c_uint64(fileId))
		else:
			return False
		 Get the current state of a workshop item.
	@staticmethod
	def GetItemState(fileId):
		if Steam.isSteamLoaded():
			return Steam.cdll.GetItemState(fileId)
		else:
			return False
	# Get the progress of an item update request.
	@staticmethod
	def GetItemUpdateProgress(updateHandle):
		if Steam.isSteamLoaded():
			bytesProcessed = pointer(c_uint64)
			bytesTotal = pointer(c_uint64)
			itemUpdateStatus = GetItemUpdateProgress(updateHandle, bytesProcessed, bytesTotal)
			# Unlike for GetItemDownloadInfo, pBytesTotal should always be set here
			progress = bytesProcessed.contents.value / bytesTotal.contents.value
			itemUpdateInfo = {
				'itemUpdateStatus' : itemUpdateStatus,
				'bytesProcessed' : bytesProcessed.contents.value,
				'bytesTotal' : bytesTotal.contents.value,
				'progress' : progress
			}
			return itemUpdateInfo
		else:
			return False
	# Set the title of a Workshop item
	@staticmethod
	def SetItemTitle(updateHandle, title):
		if Steam.isSteamLoaded():
			if len(title) > 128:
				print("ERROR: Your title is longer than 128 characters.")
				return False
			return Steam.cdll.SetItemTitle(updateHandle, title.encode())
		else:
			return False
	# Set the description of a Workshop item
	@staticmethod
	def SetItemDescription(updateHandle, description):
		if Steam.isSteamLoaded():
			if len(description) > 8000:
				print("ERROR: Your description is longer than 8000 characters.")
				return False
			return Steam.cdll.SetItemDescription(updateHandle, description.encode())
		else:
			return False
	# Set the directory containing the content you wish to upload to Workshop.
	@staticmethod
	def SetItemContent(updateHandle, contentDirectory):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemContent(updateHandle, contentDirectory.encode())
		else:
			return False
	# Set the preview image of the Workshop item.
	@staticmethod
	def SetItemPreview(updateHandle, previewImage):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemPreview(updateHandle, previewImage.encode())
		else:
			return False
	# Submit the item update with the given handle to Steam.
	@staticmethod
	def SubmitItemUpdate(updateHandle, changeNote, callback = None):
		if Steam.isSteamLoaded():
			return Steam.cdll.WSubmitItemUpdate(updateHandle, changeNote.encode())
		else:
			return False
	# Sets the language of the title and description that will be set in the item update
	@staticmethod
	def SetItemUpdateLanguage(updateHandle, language):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemUpdateLanguage(updateHandle, language)
		else:
			return False
	# Sets arbitrary metadata for an item
	@staticmethod
	def SetItemMetadata(updateHandle, metadata):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemMetadata(updateHandle, metadata)
		else:
			return False
	# Sets the visibility of an item
	@staticmethod
	def SetItemVisibility(updateHandle, visibility):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemVisibility(updateHandle, visibility)
		else:
			return False
	# Sets arbitrary developer specified tags on an item
	@staticmethod
	def SetItemTags(updateHandle, tags):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemTags(updateHandle, tags)
		else:
			return False
	# Sets the folder that will be stored as the content for an item
	@staticmethod
	def SetItemContent(updateHandle, contentFolder):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemContent(updateHandle, contentFolder)
		else:
			return False
	# Sets the primary preview image for the item
	@staticmethod
	def SetItemPreview(updateHandle, previewFile):
		if Steam.isSteamLoaded():
			return Steam.cdll.SetItemPreview(updateHandle, previewFile)
		else:
			return
	# Uploads the changes made to an item to the Steam Workshop; to be called after setting your changes
	@staticmethod
	def SubmitItemUpdate(updateHandle, changeNote):
		if Steam.isSteamLoaded():
			return Steam.cdll.SubmitItemUpdate(updateHandle, changeNote)
		else:
			return
	# Get a list of published file IDs that the user is subscribed to
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
			numItems = Steam.cdll.GetSubscribedItems(pvecPublishedFileIds, maxEntries)
			# According to steam's example, it is possible for numItems to be greater than maxEntries
			# so we crop.
			if numItems > maxEntries:
				numItems = maxEntries
			publishedFileIdsList = [pvecPublishedFileIds[i] for i in range(numItems)]
			return publishedFileIdsList
		else:
			return False
	# Get info about an installed item
	@staticmethod
	def GetItemInstallInfo(publishedFileId, maxFolderPathLength=1024):
		if Steam.isSteamLoaded():
			pSizeOnDisk = pointer(c_uint64(0))
			pTimestamp = pointer(c_uint32(0))
			pFolder = create_string_buffer(maxFolderPathLength)
			isInstalled = Steam.cdll.GetItemInstallInfo(publishedFileId, pSizeOnDisk, pFolder, maxFolderPathLength, pTimestamp)
			if isInstalled:
				itemInfo = {
					'sizeOnDisk' : pSizeOnDisk.contents.value,
					'folder' : pFolder.value.decode(),
					'timestamp' : pTimestamp.contents.value
				}
				return itemInfo
		return False
	# Get download info for a subscribed item
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