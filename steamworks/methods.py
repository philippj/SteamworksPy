from ctypes import *

STEAMWORKS_METHODS = {
    'SteamShutdown': {
        'restype': None
    },
    'RestartAppIfNecessary': {
        'restype': bool
    },
    'IsSteamRunning': {
        'restype': c_bool
    },
    'IsSubscribed': {
        'restype': bool
    },
    'IsLowViolence': {
        'restype': bool
    },
    'IsCybercafe': {
        'restype': bool
    },
    'IsVACBanned': {
        'restype': bool
    },
    'GetCurrentGameLanguage': {
        'restype': c_char_p
    },
    'GetAvailableGameLanguages': {
        'restype': c_char_p
    },
    'IsSubscribedApp': {
        'restype': bool
    },
    'IsDLCInstalled': {
        'restype': bool
    },
    'GetEarliestPurchaseUnixTime': {
        'restype': int
    },
    'IsSubscribedFromFreeWeekend': {
        'restype': bool
    },
    'GetDLCCount': {
        'restype': int
    },
    'InstallDLC': {
        'restype': None
    },
    'UninstallDLC': {
        'restype': None
    },
    'MarkContentCorrupt': {
        'restype': bool
    },
    'GetAppInstallDir': {
        'restype': c_char_p
    },
    'IsAppInstalled': {
        'restype': bool
    },
    'GetAppOwner': {
        'restype': int
    },
    'GetLaunchQueryParam': {
        'restype': c_char_p
    },
    'GetAppBuildId': {
        'restype': int
    },
    'GetFileDetails': {
        'restype': None
    },
    'GetFriendCount': {
        'restype': int
    },
    'GetFriendByIndex': {
        'restype': c_uint64
    },
    'GetPersonaName': {
        'restype': c_char_p
    },
    'GetPersonaState': {
        'restype': int
    },
    'GetFriendPersonaName': {
        'restype': c_char_p,
        'argtypes': [c_uint64]
    },
    'SetGameInfo': {
        'restype': None
    },
    'ClearGameInfo': {
        'restype': None
    },
    'InviteFriend': {
        'restype': None
    },
    'SetPlayedWith': {
        'restype': None
    },
    'ActivateGameOverlay': {
        'restype': None,
        'argtypes': [c_char_p]
    },
    'ActivateGameOverlayToUser': {
        'restype': None,
        'argtypes': [c_char_p, c_uint32]
    },
    'ActivateGameOverlayToWebPage': {
        'restype': None,
        'argtypes': [c_char_p]
    },
    'ActivateGameOverlayToStore': {
        'restype': None,
        'argtypes': [c_uint32]
    },
    'ActivateGameOverlayInviteDialog': {
        'restype': None,
        'argtypes': [c_uint64]
    },
    'ActivateActionSet': {
        'restype': None
    },
    'GetActionSetHandle': {
        'restype': c_uint64
    },
    'GetAnalogActionHandle': {
        'restype': c_uint64
    },
    'GetControllerForGamepadIndex': {
        'restype': c_uint64
    },
    'GetCurrentActionSet': {
        'restype': c_uint64
    },
    'GetInputTypeForHandle': {
        'restype': c_uint64
    },
    'GetDigitalActionHandle': {
        'restype': c_uint64
    },
    'GetGamepadIndexForController': {
        'restype': int
    },
    'ControllerInit': {
        'restype': bool
    },
    'RunFrame': {
        'restype': None
    },
    'ShowBindingPanel': {
        'restype': bool
    },
    'ControllerShutdown': {
        'restype': bool
    },
    'TriggerVibration': {
        'restype': None
    },
    'CreateLobby': {
        'restype': None,
        'argtypes': [c_uint64, c_uint64]
    },
    'JoinLobby': {
        'restype': None,
        'argtypes': [c_uint64]
    },
    'LeaveLobby': {
        'restype': None,
        'argtypes': [c_uint64]
    },
    'InviteUserToLobby': {
        'restype': None,
        'argtypes': [c_uint64, c_uint64]
    },
    'MusicIsEnabled': {
        'restype': None
    },
    'MusicIsPlaying': {
        'restype': None
    },
    'MusicGetVolume': {
        'restype': c_float
    },
    'MusicPause': {
        'restype': None
    },
    'MusicPlay': {
        'restype': None
    },
    'MusicPlayNext': {
        'restype': None
    },
    'MusicPlayPrev': {
        'restype': None
    },
    'MusicSetVolume': {
        'restype': None
    },
    'AddScreenshotToLibrary': {
        'restype': c_uint32
    },
    'HookScreenshots': {
        'restype': None
    },
    'IsScreenshotsHooked': {
        'restype': bool
    },
    'SetLocation': {
        'restype': None
    },
    'TriggerScreenshot': {
        'restype': None
    },
    'GetSteamID': {
        'restype': c_uint64
    },
    'LoggedOn': {
        'restype': bool
    },
    'GetPlayerSteamLevel': {
        'restype': int
    },
    'GetUserDataFolder': {
        'restype': c_char_p
    },
    'GetGameBadgeLevel': {
        'restype': int
    },
    'GetAchievement': {
        'restype': bool
    },
    'GetNumAchievements': {
        'restype': int
    },
    'GetAchievementName': {
        'restype': c_char_p
    },
    'GetAchievementDisplayAttribute': {
        'restype': c_char_p
    },
    'GetStatInt': {
        'restype': int
    },
    'GetStatFloat': {
        'restype': c_float
    },
    'ResetAllStats': {
        'restype': bool
    },
    'RequestCurrentStats': {
        'restype': bool
    },
    'SetAchievement': {
        'restype': bool
    },
    'SetStatInt': {
        'restype': bool
    },
    'SetStatFloat': {
        'restype': bool
    },
    'StoreStats': {
        'restype': bool
    },
    'ClearAchievement': {
        'restype': bool
    },
    'Leaderboard_FindLeaderboard': {
        'restype': bool,
        'argtypes': [c_char_p]
    },
    'OverlayNeedsPresent': {
        'restype': bool
    },
    'GetAppID': {
        'restype': int
    },
    'GetCurrentBatteryPower': {
        'restype': int
    },
    'GetIPCCallCount': {
        'restype': c_uint32
    },
    'GetIPCountry': {
        'restype': c_char_p
    },
    'GetSecondsSinceAppActive': {
        'restype': int
    },
    'GetSecondsSinceComputerActive': {
        'restype': int
    },
    'GetServerRealTime': {
        'restype': int
    },
    'GetSteamUILanguage': {
        'restype': c_char_p
    },
    'IsOverlayEnabled': {
        'restype': bool
    },
    'IsSteamInBigPictureMode': {
        'restype': bool
    },
    'IsSteamRunningInVR': {
        'restype': bool
    },
    'IsVRHeadsetStreamingEnabled': {
        'restype': bool
    },
    'SetOverlayNotificationInset': {
        'restype': None
    },
    'SetOverlayNotificationPosition': {
        'restype': None
    },
    'SetVRHeadsetStreamingEnabled': {
        'restype': None
    },
    'ShowGamepadTextInput': {
        'restype': bool
    },
    'StartVRDashboard': {
        'restype': None
    },
    'Workshop_StartItemUpdate': {
        'restype': c_uint64
    },
    'Workshop_SetItemTitle': {
        'restype': bool,
        'argtypes': [c_uint64, c_char_p]
    },
    'Workshop_SetItemDescription': {
        'restype': bool,
        'argtypes': [c_uint64, c_char_p]
    },
    'Workshop_SetItemUpdateLanguage': {
        'restype': bool
    },
    'Workshop_SetItemMetadata': {
        'restype': bool
    },
    'Workshop_SetItemVisibility': {
        'restype': bool
    },
    'Workshop_SetItemTags': {
        'restype': bool
    },
    'Workshop_SetItemContent': {
        'restype': bool,
        'argtypes': [c_uint64, c_char_p]
    },
    'Workshop_SetItemPreview': {
        'restype': bool,
        'argtypes': [c_uint64, c_char_p]
    },
    'Workshop_SubmitItemUpdate': {
        'argtypes': [c_uint64, c_char_p]
    },
    'Workshop_GetNumSubscribedItems': {
        'restype': c_uint32
    },
    'Workshop_GetSubscribedItems': {
        'restype': c_uint32,
        'argtypes': [POINTER(c_uint64), c_uint32]
    },
    'Workshop_GetItemState': {
        'restype': c_uint32,
        'argtypes': [c_uint64]
    },
    'Workshop_GetItemInstallInfo': {
        'restype': bool,
        'argtypes': [c_uint64, POINTER(c_uint64), c_char_p, c_uint32,  POINTER(c_uint32)]
    },
    'Workshop_GetItemDownloadInfo': {
        'restype': bool,
        'argtypes': [c_uint64, POINTER(c_uint64), POINTER(c_uint64)]
    },
    'Workshop_SuspendDownloads': {
        'restype': None,
        'argtypes': [c_bool]
    },
    'Workshop_SubscribeItem': {
        'restype': None,
        'argtypes': [c_uint64]
    },
    'Workshop_UnsubscribeItem': {
        'restype': None,
        'argtypes': [c_uint64]
    }
}
