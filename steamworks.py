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
		if sys.maxsize > 2**32 is False:
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
		Steam.cdll.ActivateGameOverlay.restype = c_char_p
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

	@staticmethod
	def Call(method):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return method()

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