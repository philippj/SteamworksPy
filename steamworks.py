#!/usr/bin/python
# -*- coding: utf-8 -*-
# Steamworks for Python

from ctypes import *
import platform

PersonaState = {
    0x00: 'Offline',
    0x01: 'Online',
    0x02: 'Busy',
    3: 'Away',
    0x04: 'Snooze',
    5: 'Looking to Trade',
    6: 'Looking to Play',
    }

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


class Steam:

    cdll = None
    player_un = None
    warn = False
    loaded = False

    @staticmethod
    def Init():
        if platform.system() == 'Windows':
            Steam.cdll = CDLL('SteamPy.dll')
            print('Steam loaded for Windows')
            Steam.loaded = True
        elif platform.system() == 'Linux':
            Steam.cdll = CDLL('libsteampy.so')
            print('Steam loaded for Linux')
            Steam.loaded = True
        else:
            print('Steam load fail (unsupported platform)')
            Steam.warn = True
            return
        Steam.cdll.SteamInit()
        Steam.cdll.IsFriendInGame.restype = bool
        Steam.cdll.GetPersonaName.restype = c_char_p
        Steam.cdll.GetFriendNameByIndex.restype = c_char_p
        Steam.cdll.GetFriendGame.restype = long
        Steam.cdll.IsOverlayEnabled.restype = bool
        Steam.cdll.GetIPCountry.restype = c_char_p
        Steam.cdll.IsSteamRunningInVR.restype = bool

        Steam.cdll.MusicIsEnabled.restype = bool
        Steam.cdll.MusicIsPlaying.restype = bool
        Steam.cdll.MusicGetVolume.restype = c_float

        Steam.cdll.GetStatInt.restype = int
        Steam.cdll.GetStatFloat.restype = float
        Steam.cdll.SetStatInt.restype = bool
        Steam.cdll.SetStatFloat.restype = bool
        Steam.cdll.StoreStats.restype = bool
        Steam.cdll.RequestCurrentStats = bool
        Steam.cdll.SetAchievement = bool
        Steam.cdll.GetAchievement = bool

    @staticmethod
    def Call(method):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return method()


class SteamFriends:

    @staticmethod
    def GetPlayerName():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            name = \
                (Steam.cdll.GetPersonaName() if not Steam.player_un else Steam.player_un)
            Steam.player_un = \
                (name if not Steam.player_un else Steam.player_un)
            return name

    @staticmethod
    def GetFriendCount(flag=FriendFlags['All']):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetFriendCount(flag)

    @staticmethod
    def GetFriendNameByIndex(index, flag=FriendFlags['All']):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            if type(index) is int:
                return Steam.cdll.GetFriendNameByIndex(index, flag)

    @staticmethod
    def GetFriendList(flag=FriendFlags['All']):
        l = list()
        for i in range(0x00, SteamFriends.GetFriendCount(flag) - 0x01):
            l.append(SteamFriends.GetFriendNameByIndex(i, flag))
        return l

    @staticmethod
    def GetFriendPersonaStateByIndex(index, string=True,
            flag=FriendFlags['All']):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            state = Steam.cdll.GetFriendStateByIndex(index, flag)
            return (PersonaState[state] if string else state)

    @staticmethod
    def GetPersonaState(string=True):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            state = Steam.cdll.GetPersonaState()
            return (PersonaState[state] if string else state)

    @staticmethod
    def GetFriendGameByIndex(index, flag=FriendFlags['All']):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetFriendGame(index, flag)

    @staticmethod
    def IsFriendInGameByIndex(index, flag=FriendFlags['All']):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.IsFriendInGame(index, flag)

    @staticmethod
    def SetPersonaName(newname):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            Steam.cdll.SetPersonaName(newname)


class SteamUtils:

    @staticmethod
    def IsOverlayEnabled():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.IsOverlayEnabled()

    @staticmethod
    def GetCurrentBatteryPower():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetCurrentBatteryPower()

    @staticmethod
    def GetSecondsSinceAppActive():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetSecondsSinceAppActive()

    @staticmethod
    def GetSecondsSinceComputerActive():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetSecondsSinceComputerActive()

    @staticmethod
    def GetServerRealTime():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetServerRealTime()

    @staticmethod
    def GetIPCountry():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetIPCountry()

    @staticmethod
    def IsSteamRunningInVR():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.IsSteamRunningInVR()


class SteamMusic:

    @staticmethod
    def Play():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicPlay()

    @staticmethod
    def Pause():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicPause()

    @staticmethod
    def PlayNext():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicPlayNext()

    @staticmethod
    def PlayPrevious():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicPlayPrev()

    @staticmethod
    def GetVolume():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicGetVolume()

    @staticmethod
    def SetVolume(vol):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicSetVolume()

    @staticmethod
    def IsEnabled():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicIsEnabled()

    @staticmethod
    def IsPlaying():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.MusicIsPlaying()


class SteamUserStats:
    @staticmethod
    def GetStatInt(name):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetStatInt(name)
    @staticmethod
    def GetStatFloat(name):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetStatFloat(name)
    @staticmethod
    def SetStat(name, value):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
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
    def GetAchievement(name):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.GetAchievement(name)

    @staticmethod
    def SetAchievement(name):
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.SetAchievement(name)
    @staticmethod
    def RequestCurrentStats():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.RequestCurrentStats()
    @staticmethod
    def StoreStats():
        if not Steam.cdll and not Steam.warn:
            print('Steam is not loaded')
            Steam.warn = True
            return False
        else:
            return Steam.cdll.StoreStats()

