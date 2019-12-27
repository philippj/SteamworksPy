from enum import Enum


class Arch(Enum):
    """ Limited list of processor architectures """
    x86 = 0
    x64 = 1


class FriendFlags(Enum):
    """ EFriendFlags """
    NONE                    = 0x00
    BLOCKED                 = 0x01
    FRIENDSHIP_REQUESTED    = 0x02
    IMMEDIATE               = 0x04
    CLAN_MEMBER             = 0x08
    ON_GAME_SERVER          = 0x10
    REQUESTING_FRIENDSHIP   = 0x80
    REQUESTING_INFO         = 0x100
    IGNORED                 = 0x200
    IGNORED_FRIEND          = 0x400
    SUGGESTED               = 0x800
    ALL                     = 0xFFFF


class EWorkshopFileType(Enum):
    COMMUNITY               = 0x01
    COLLECTION              = 0x02
    ART                     = 0x03
    VIDEO                   = 0x04
    SCREENSHOT              = 0x05
    GAME                    = 0x06
    SOFTWARE                = 0x07
    CONCEPT                 = 0x08
    WEB_GUIDE               = 0x09
    INTEGRATED_GUIDE        = 0x10
    MERCH                   = 0x11
    CONTROLLER_BINDING      = 0x12
    STEAMWORKS_ACCESS_INVITE = 0x13
    STEAM_VIDEO             = 0x14
    GAME_MANAGED_ITEM       = 0x15
    MAX                     = 0x16


class EItemState(Enum):
    """ EItemState """
    NONE                = 0
    SUBSCRIBED          = 1
    LEGACY_ITEM         = 2
    INSTALLED           = 4
    NEEDS_UPDATE        = 8
    DOWNLOADING         = 16
    DOWNLOAD_PENDING    = 32


class ENotificationPosition(Enum):
    TOP_LEFT        = 0
    TOP_RIGHT       = 1
    BOTTOM_LEFT     = 2
    BOTTOM_RIGHT    = 3


class EGamepadTextInputLineMode(Enum):
    SINGLE_LINE     = 0
    MULTIPLE_LINES  = 1


class EGamepadTextInputMode(Enum):
    NORMAL      = 0
    PASSWORD    = 1


class EItemUpdateStatus(Enum):
    INVALID                 = 0
    PREPARING_CONFIG        = 1
    PREPARING_CONTENT       = 2
    UPLOADING_CONTENT       = 3
    UPLOADING_PREVIEW_FILE  = 4
    COMMITTING_CHANGES      = 5
