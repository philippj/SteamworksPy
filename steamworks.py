#================================================
# Steamworks For Python
#================================================
from ctypes import *
import sys, os

# User status
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

WorkshopFileType = {
	'Community': 0x00,			# normal Workshop item that can be subscribed to
	'Microtransaction': 0x01,	# Workshop item that is meant to be voted on for the purpose of selling in-game

	# NOTE: There are more workshop file types defined "in isteamremotestorage.h",
	# but we do not need them for now.
}

WorkshopItemState = {
	"ItemStateNone":			0,	# item not tracked on client
	"ItemStateSubscribed":		1,	# current user is subscribed to this item. Not just cached.
	"ItemStateLegacyItem":		2,	# item was created with ISteamRemoteStorage
	"ItemStateInstalled":		4,	# item is installed and usable (but maybe out of date)
	"ItemStateNeedsUpdate":		8,	# items needs an update. Either because it's not installed yet or creator updated content
	"ItemStateDownloading":		16,	# item update is currently downloading
	"ItemStateDownloadPending":	32,	# DownloadItem() was called for this item, content isn't available until DownloadItemResult_t is fired
}

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
		if (sys.maxsize > 2**32) is False:
			OS_BIT = '32bits'
		else:
			OS_BIT = '64bits'
		# Loading SteamPy API for Linux
		if sys.platform == 'linux' or sys.platform == 'linux2':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.so"))
			print("SteamworksPy loaded for Linux")
			Steam.loaded = True
		# Loading SteamPy API for Mac
		elif sys.platform == 'darwin':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dylib" ))
			print("SteamworksPy loaded for Mac")
			Steam.loaded = True
		# Loading Steamworks API for Windows
		elif sys.platform == 'win32':
			# Check Windows architecture
			if OS_BIT == '32bits':
				Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy.dll"))
			else:
				Steam.cdll = CDLL(os.path.join(os.getcwd(), "SteamworksPy64.dll"))
			print("SteamworksPy loaded for Windows")
			Steam.loaded = True
		# Unrecognized platform, warn user and do not load Steam API
		else:
			print("SteamworksPy failed to load (unsupported platform!")
			Steam.warn = True
			return

		# Set restype for initialization
		Steam.cdll.IsSteamRunning.restype = c_bool
		# Check that Steam is running
		if Steam.cdll.IsSteamRunning():
			print("Steam is running!")
		else:
			print("Steam is not running!")

		# Boot up the Steam API
		Steam.cdll.SteamInit()
		# Set restype for Apps functions
		Steam.cdll.GetDlcCount.restype = int
		Steam.cdll.IsDlcInstalled.restype = bool
		Steam.cdll.RequestAppProofOfPurchaseKey.restype = c_char_p
		# Set restype for Friends functions
		Steam.cdll.GetFriendCount.restype = int
		Steam.cdll.GetPersonaName.restype = c_char_p
		Steam.cdll.GetPersonaState.restype = int
		Steam.cdll.ActivateGameOverlay.restype = None
		Steam.cdll.ActivateGameOverlayToWebPage.restype = None
		# Set restype for Music functions
		Steam.cdll.MusicIsEnabled.restype = bool
		Steam.cdll.MusicIsPlaying.restype = bool
		Steam.cdll.MusicGetVolume.restype = c_float
		Steam.cdll.MusicPause.restype = bool
		Steam.cdll.MusicPlay.restype = bool
		Steam.cdll.MusicPlayNext.restype = bool
		Steam.cdll.MusicPlayPrev.restype = bool
		Steam.cdll.MusicSetVolume.restype = c_float
		# Set restype for User functions		
		Steam.cdll.GetSteamID.restype = int
		Steam.cdll.GetPlayerSteamLevel.restype = int
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

	@staticmethod
	def isSteamLoaded():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return True

	@staticmethod
	def Call(method):
		if Steam.isSteamLoaded():
			return method()
		else:
			return False

	@staticmethod
	def RunCallbacks():
		if Steam.isSteamLoaded():
			Steam.cdll.RunCallbacks()
			return True
		else:
			return False

# Class for Steam Apps
#------------------------------------------------
class SteamApps:

	@staticmethod
	def GetDlcCount():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetDlcCount()

	@staticmethod
	def IsDlcInstalled():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.IsDlcInstalled()

	@staticmethod
	def RequestAppProofOfPurchaseKey():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.RequestAppProofOfPurchaseKey()

# Class for Steam Friends
#------------------------------------------------
class SteamFriends:

	@staticmethod
	def GetFriendCount(flag=FriendFlags['All']):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetFriendCount(flag)

	@staticmethod
	def GetPlayerName():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetPersonaName()

	@staticmethod
	def GetPlayerState():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetPersonaState()

	@staticmethod
	def ActivateGameOverlay():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.ActivateGameOverlay()	

	@staticmethod
	def ActivateGameOverlayToWebPage(url):
		if Steam.isSteamLoaded():
			return Steam.cdll.ActivateGameOverlayToWebPage(url)
		else:
			return False

# Class for Steam Music
class SteamMusic:

	@staticmethod
	def MusicIsEnabled():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicIsEnabled()

	@staticmethod
	def MusicIsPlaying():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicIsPlaying()

	@staticmethod
	def MusicGetVolume():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicGetVolume()

	@staticmethod
	def MusicPause():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPause()

	@staticmethod
	def MusicPlay():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlay()

	@staticmethod
	def MusicPlayNext():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlayNext()

	@staticmethod
	def MusicPlayPrev():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlayPrev()

	@staticmethod
	def MusicSetVolume(value):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicSetVolume(value)

# Class for Steam Users
#------------------------------------------------
class SteamUser:

	@staticmethod
	def GetPlayerID():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetSteamID()

	@staticmethod
	def GetPlayerSteamLevel():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetPlayerSteamLevel()

# Class for Steam User Statistics
#------------------------------------------------
class SteamUserStats:

	@staticmethod
	def GetAchievement(name):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetAchievement(name)

	@staticmethod
	def GetStatFloat(name):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetStatFloat(name)

	@staticmethod
	def GetStatInt(name):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetStatInt(name)

	@staticmethod
	def ResetAllStats(achievesToo):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.ResetAllStats(achievesToo)

	@staticmethod
	def RequestCurrentStats():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.RequestCurrentStats()

	@staticmethod
	def SetAchievement(name):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.SetAchievement(name)

	@staticmethod
	def SetStat(name, value):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			if isinstance(value, float):
				return Steam.cdll.SetStatFloat(name, value)
			elif isinstance(value, int):
				return Steam.cdll.SetStatInt(name, value)
			else:
				raise Exception("SteamUserStats: SetStat value can be only int or float.")

	@staticmethod
	def StoreStats():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.StoreStats()

	@staticmethod
	def ClearAchievement(name):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.ClearAchievement(name)

# Class for Steam Workshop
#------------------------------------------------
class SteamWorkshop:
	class CreateItemResult_t(Structure):
		"""A class that describes Steam's CreateItemResult_t C struct"""
		_fields_ = [
			("result", c_int),
			("publishedFileId", c_uint64),
			("userNeedsToAcceptWorkshopLegalAgreement", c_bool)
		]

	class SubmitItemUpdateResult_t(Structure):
		"""A class that describes Steam's SubmitItemUpdateResult_t C struct"""
		_fields_ = [
			("result", c_int),
			("userNeedsToAcceptWorkshopLegalAgreement", c_bool)
		]

	class ItemInstalled_t(Structure):
		"""A class that describes Steam's ItemInstalled_t C struct"""
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

	@staticmethod
	def SetItemCreatedCallback(callback):
		if Steam.isSteamLoaded():
			SteamWorkshop.itemCreatedCallback = SteamWorkshop.ITEM_CREATED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemCreatedCallback(SteamWorkshop.itemCreatedCallback)
		else:
			return False

	@staticmethod
	def SetItemUpdatedCallback(callback):
		if Steam.isSteamLoaded():
			SteamWorkshop.itemUpdatedCallback = SteamWorkshop.ITEM_UPDATED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemUpdatedCallback(SteamWorkshop.itemUpdatedCallback)
		else:
			return False

	@classmethod
	def SetItemInstalledCallback(cls, callback):
		if Steam.isSteamLoaded():
			cls.itemInstalledCallback = cls.ITEM_INSTALLED_CALLBACK_TYPE(callback)

			Steam.cdll.Workshop_SetItemInstalledCallback(cls.itemInstalledCallback)
		else:
			return False

	@classmethod
	def ClearItemInstalledCallback(cls, callback):
		if Steam.isSteamLoaded():
			itemInstalledCallback = None
			Steam.cdll.Workshop_ClearItemInstalledCallback()

	@staticmethod
	def CreateItem(appId, filetype, callback = None):
		"""Create a UGC (Workshop) item

		Arguments:
		
		appId -- The app ID of the game on Steam. 
		Do not use the creation tool app ID if they are separate.

		filetype -- Can be a community file type or microtransactions.
		Use predefined `WorkshopFileType` values.

		callback -- The function to call once the item creation is finished.
		"""
		if Steam.isSteamLoaded():
			if callback != None:
				SteamWorkshop.SetItemCreatedCallback(callback)

			Steam.cdll.Workshop_CreateItem(appId, filetype)
			return True
		else:
			return False

	@staticmethod
	def StartItemUpdate(appId, publishedFileId):
		"""Start the item update process and receive an update handle.

		Arguments:

		appId -- The app ID of the game on Steam. 
		Do not use the creation tool app ID if they are separate

		publishedFileId -- The ID of the Workshop file you are updating

		Return value:
		
		If sucessful: update handle - an ID of the current update transaction
		Otherwise: False
		"""
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_StartItemUpdate(appId, c_uint64(publishedFileId))
		else:
			return False

	@staticmethod
	def SetItemTitle(updateHandle, title):
		"""Set the title of a Workshop item

		Arguments:

		updateHandle -- the handle returned by 'StartItemUpdate'

		title -- the desired title of the item.

		Return value:

		True on succes,
		False otherwise.
		"""
		if Steam.isSteamLoaded():
			if len(title) > 128:
				print("ERROR: Your title is longer than 128 characters.")
				return False

			return Steam.cdll.Workshop_SetItemTitle(updateHandle, title.encode())
		else:
			return False

	@staticmethod
	def SetItemDescription(updateHandle, description):
		"""Set the description of a Workshop item

		Arguments:

		updateHandle -- the handle returned by 'StartItemUpdate'

		description -- the desired description of the item.

		Return value:

		True on succes,
		False otherwise.
		"""
		if Steam.isSteamLoaded():
			if len(description) > 8000:
				print("ERROR: Your description is longer than 8000 characters.")
				return False

			return Steam.cdll.Workshop_SetItemDescription(updateHandle, description.encode())
		else:
			return False

	@staticmethod
	def SetItemContent(updateHandle, contentDirectory):
		"""Set the directory containing the content you wish to upload to Workshop.

		Arguments:

		updateHandle -- the handle returned by 'StartItemUpdate'

		contentDirectory -- path to the directory containing the content of the workshop item.

		Return value:

		True on succes,
		False otherwise.
		"""
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_SetItemContent(updateHandle, contentDirectory.encode())
		else:
			return False

	@staticmethod
	def SetItemPreview(updateHandle, previewImage):
		"""Set the preview image of the Workshop item.

		Arguments:

		updateHandle -- the handle returned by 'StartItemUpdate'

		previewImage -- path to the preview image file.

		Return value:

		True on succes,
		False otherwise.
		"""
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_SetItemPreview(updateHandle, previewImage.encode())
		else:
			return False

	@staticmethod
	def SubmitItemUpdate(updateHandle, changeNote, callback = None):
		"""Submit the item update with the given handle to Steam.

		Arguments:

		updateHandle -- the handle returned by 'StartItemUpdate'

		changeNote -- a string containing change notes for the current update.
		"""
		if Steam.isSteamLoaded():
			if callback != None:
				SteamWorkshop.SetItemUpdatedCallback(callback)

			return Steam.cdll.Workshop_SubmitItemUpdate(updateHandle, changeNote.encode())
		else:
			return False

	@staticmethod
	def GetItemUpdateProgress(updateHandle):
		"""Get the progress of an item update request.

		Argument:

		updateHandle -- the handle returned by 'StartItemUpdate'

		Return Value:

		On success: An object with the following attributes

		-- 'itemUpdateStatus - a `WorkshopItemUpdateStatus` value describing the update status of the item
		-- 'bytesProcessed' - amount of bytes processed
		-- 'bytesTotal' - total amount of bytes to be processed
		-- 'progress' - a value ranging from 0 to 1 representing update progress

		Otherwise: False
		"""
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

	@staticmethod
	def GetNumSubscribedItems():
		"""Get the total number of items the user is subscribed to for this game or application.

		Return value:

		On success: The number of subscribed items,
		Otherwise: False.
		"""
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_GetNumSubscribedItems()
		else:
			return False

	@staticmethod
	def GetSubscribedItems(maxEntries=-1):
		"""Get a list of published file IDs that the user is subscribed to

		Arguments:

		maxEntries -- the maximum number of entries to fetch. If omitted
		the function will try to fetch as much items as the user is 
		subscribed to.

		Return Value:

		On success: A list of published file IDs that the user is subscribed to.
		Otherwise: False.
		"""
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

	@staticmethod
	def GetItemState(publishedFileId):
		"""Get the current state of a workshop item.

		Arguments:

		publishedFileId -- the id of the item whose state to check

		Return Value:

		On success: A `WorkshopItemState` value describing the item state.
		Otherwise: False
		"""
		if Steam.isSteamLoaded():
			return Steam.cdll.Workshop_GetItemState(publishedFileId)
		else:
			return False

	@staticmethod
	def GetItemInstallInfo(publishedFileId, maxFolderPathLength=1024):
		"""Get info about an installed item

		Arguments:

		publishedFileId -- the id of the item to look up,
		maxFolderPathLength -- maximum length of the folder path in characters.

		Return Value:

		If the item is installed: an object with the following attributes
		-- 'sizeOnDisk'
		-- 'folder'
		-- 'timestamp'

		If the item is not installed, or the method fails it returns: False
		"""
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

	@staticmethod
	def GetItemDownloadInfo(publishedFileId):
		"""Get download info for a subscribed item

		Arguments:

		publishedFileId -- the id of the item whose download info to look up

		Return Value:

		If download information is available returns an object with
		the following attributes

		-- 'bytesDownloaded'- the amount of downloaded bytes
		-- 'bytesTotal' - the total amounts of bytes an item has
		-- 'progress' - a value ranging from 0 to 1 representing download progress

		If download information or steamworks or not available, 
		returns False
		"""
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

# Class for Steam Utilities
#------------------------------------------------
class SteamUtilities:
	
	@staticmethod
	def GetCurrentBatteryPower():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetCurrentBatteryPower()

	@staticmethod
	def GetIPCountry():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetIPCountry()

	@staticmethod
	def GetSecondsSinceAppActive():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetSecondsSinceAppActive()

	@staticmethod
	def GetSecondsSinceComputerActive():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetSecondsSinceComputerActive()

	@staticmethod
	def GetServerRealTime():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetServerRealTime()

	@staticmethod
	def IsOverlayEnabled():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.IsOverlayEnabled()

	@staticmethod
	def IsSteamRunningInVR():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.IsSteamRunningInVR()

	@staticmethod
	def GetSteamUILanguage():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetSteamUILanguage()

	@staticmethod
	def GetAppID():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetAppID()
