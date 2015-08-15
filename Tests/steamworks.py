#================================================
# Steamworks For Python
#================================================
from ctypes import *
import sys, os

# User's status
#------------------------------------------------
PersonaState = {
	0x00: 'Offline',
	0x01: 'Online',
	0x02: 'Busy',
	3: 'Away',
	0x04: 'Snooze',
	5: 'Looking to Trade',
	6: 'Looking to Play',
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
		# Loading SteamPy API for Linux
		if sys.platform == 'linux' or sys.platform == 'linux2':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "libsteampy.so"))
			print("SteamPy loaded for Linux")
			Steam.loaded = True
		# Loading SteamPy API for Mac
		elif sys.platform == 'darwin':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "libsteampy.dylib" ))
			print("SteamPy loaded for Mac")
			Steam.loaded = True
		# Loading SteamPy API for Windows
		elif sys.platform == 'win32':
			Steam.cdll = CDLL(os.path.join(os.getcwd(), "steampy.dll"))
			print("SteamPy loaded for Windows")
			Steam.loaded = True
		# Unrecognized platform, warn user and do not load Steam API
		else:
			print("SteamPy failed to load (unsupported platform!")
			Steam.warn = True
			return

		# Set restype for initialization
		Steam.cdll.SteamAPI_IsSteamRunning.restype = c_bool
		# Check that Steam is running
		if Steam.cdll.SteamAPI_IsSteamRunning():
			print("Steam is running!")
		else:
			print("Steam is not running!")

		# Boot up the Steam API
		Steam.cdll.SteamInit()

		# Set restype for App functions
		Steam.cdll.GetDLCCount.restype = int
		Steam.cdll.IsDlcInstalled = bool
		# Set restype for Friends functions
		Steam.cdll.GetFriendCount.restype = int
		Steam.cdll.GetPersonaName.restype = c_char_p
		Steam.cdll.GetPersonaState.restype = int
		# Set restype for Music functions
		Steam.cdll.MusicIsEnabled.restype = bool
		Steam.cdll.MusicIsPlaying.restype = bool
		Steam.cdll.MusicGetVolume.restype = c_float
		# Set restype for User functions		
		Steam.cdll.GetSteamID.restype = int
		# Set restype for User Statistic functions
		Steam.cdll.GetAchievement = bool
		Steam.cdll.GetStatFloat.restype = float
		Steam.cdll.GetStatInt.restype = int
		Steam.cdll.RequestCurrentStats.restype = bool
		Steam.cdll.SetAchievement.restype = bool
		Steam.cdll.SetStatFloat.restype = bool
		Steam.cdll.SetStatInt.restype = bool
		Steam.cdll.StoreStats.restype = bool
		# Set restype for Utility functions
		Steam.cdll.GetCurrentBatteryPower.restype = int
		Steam.cdll.GetIPCountry.restype = c_char_p
		Steam.cdll.GetSecondsSinceAppActive.restype = int
		Steam.cdll.GetSecondsSinceComputerActive.restype = int
		Steam.cdll.GetServerRealTime.restype = int
		Steam.cdll.IsOverlayEnabled.restype = bool
		Steam.cdll.IsSteamRunningInVR.restype = bool

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
	def GetDLCCount():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetDLCCount()

	# The App ID of the DLC itself
	@staticmethod
	def IsDlcInstalled(appID):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.IsDlcInstalled(appID)

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
	def GetPersonaState(string=True):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			state = Steam.cdll.GetPersonaState()
			return (PersonaState[state] if string else state)

# Class for Steam Music
#------------------------------------------------
class SteamMusic:

	@staticmethod
	def IsEnabled():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicIsEnabled()

	@staticmethod
	def IsPlaying():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicIsPlaying()

	@staticmethod
	def GetVolume():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicGetVolume()

	@staticmethod
	def Pause():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPause()

	@staticmethod
	def Play():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlay()

	@staticmethod
	def PlayNext():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlayNext()

	@staticmethod
	def PlayPrevious():
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicPlayPrev()

	@staticmethod
	def SetVolume(vol):
		if not Steam.cdll and not Steam.warn:
			print("Steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.MusicSetVolume(vol)

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

# Class for Steam Utilties
#------------------------------------------------
class SteamUtils:

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