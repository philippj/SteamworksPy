#Steamworks for Python

from ctypes import *
import platform

PersonaState = {
	0 : "Offline",
	1 : "Online",
	2 : "Busy",
	3 : "Away",
	4 : "Snooze",
	5 : "Looking to Trade",
	6 : "Looking to Play"
}

FriendFlags = {
	"None" : 0x00,
	"Blocked" : 0x01,
	"FriendshipRequested" : 0x02,
	"Immediate" : 0x04, #regular friend
	"ClanMember" : 0x08,
	"OnGameServer" : 0x10,
	"RequestingFriendship" : 0x80,
	"RequestingInfo" : 0x100,
	"Ignored" : 0x200,
	"IgnoredFriend" : 0x400,
	"Suggested" : 0x800,
	"All" : 0xFFFF
}

class Steam:
	cdll = None
	player_un = None
	warn = False
	loaded = False
	@staticmethod 
	def Init():
		if platform.system() == "Windows":
			Steam.cdll = CDLL("SteamPy.dll")
			print("steam loaded for windows")
			Steam.loaded = True
		elif platform.system() == "Linux":
			Steam.cdll = CDLL("libsteampy.so")
			print("steam loaded for linux")
			Steam.loaded = True
		else:
			print("steam load fail (unsupported platform)")
			Steam.warn = True
			return
		Steam.cdll.SteamInit()
	@staticmethod 
	def GetPlayerName():
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			Steam.cdll.GetPersonaName.restype = c_char_p
			name = Steam.cdll.GetPersonaName() if not Steam.player_un else Steam.player_un
			Steam.player_un = name if not Steam.player_un else Steam.player_un
			return(name)

	@staticmethod 
	def GetFriendCount(flag = FriendFlags["All"]):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			return Steam.cdll.GetFriendCount(flag)

	@staticmethod 
	def GetFriendNameByIndex(index, flag = FriendFlags["All"]):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			if type(index) is int:
				Steam.cdll.GetFriendNameByIndex.restype = c_char_p
				return Steam.cdll.GetFriendNameByIndex(index, flag)

	@staticmethod 
	def GetFriendList(flag = FriendFlags["All"]):
		l = list()
		for i in range(0, Steam.GetFriendCount(flag)-1):
			l.append(Steam.GetFriendNameByIndex(i, flag))
		return l

	@staticmethod 
	def GetFriendPersonaStateByIndex(index, string = True, flag = FriendFlags["All"]):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			state = Steam.cdll.GetFriendStateByIndex(index, flag)
			return PersonaState[state] if string else state

	@staticmethod 
	def GetPersonaState(string = True):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			state = Steam.cdll.GetPersonaState()
			return PersonaState[state] if string else state

	@staticmethod 
	def GetFriendGameByIndex(index, flag = FriendFlags["All"]):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			Steam.cdll.GetFriendGame.restype = long
			return Steam.cdll.GetFriendGame(index, flag)

	@staticmethod 
	def IsFriendInGameByIndex(index, flag = FriendFlags["All"]):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			Steam.cdll.IsFriendInGame.restype = bool
			return Steam.cdll.IsFriendInGame(index, flag)

	@staticmethod 
	def SetPersonaName(newname):
		if not Steam.cdll and (not Steam.warn):
			print("steam is not loaded")
			Steam.warn = True
			return False
		else:
			Steam.cdll.SetPersonaName.restype = None
			Steam.cdll.SetPersonaName(newname)
