/////////////////////////////////////////////////
//  STEAMWORKSPY - STEAMWORKS FOR PYTHON
/////////////////////////////////////////////////
//
// Modify SW_PY based on operating system and include the proper Steamworks API file
//
// Include the Steamworks API header
#if defined( _WIN32 )
	#include "steam\steam_api.h"
	#define SW_PY extern "C" __declspec(dllexport)
#elif defined( __APPLE__ )
	#include "steam/steam_api.h"
	#include "TargetConditionals.h"
	#define SW_PY extern "C" __attribute__ ((visibility("default")))
#elif defined( __linux__ )
	#include "steam/steam_api.h"
	#define SW_PY extern "C" __attribute__ ((visibility("default")))
#else
	#error "Unsupported platform"
#endif

#include <iostream>

// Enumerated constants /////////////////////////
enum {
	OFFLINE=0, ONLINE=1, BUSY=2, AWAY=3, SNOOZE=4, LF_TRADE, LF_PLAY, STATE_MAX, NOT_OFFLINE=8, ALL=9,
	TOP_LEFT=0, TOP_RIGHT=1, BOT_LEFT=2, BOT_RIGHT=3,
	FLAG_NONE=0x00, FLAG_BLOCKED=0x01, FLAG_FRIENDSHIP_REQUESTED=0x02, FLAG_IMMEDIATE=0x04, FLAG_CLAN_MEMBER=0x08, FLAG_ON_GAME_SERVER=0x10, FLAG_REQUESTING_FRIENDSHIP=0x80, FLAG_REQUESTING_INFO=0x100,
	FLAG_IGNORED=0x200, FLAG_IGNORED_FRIEND=0x400, FLAG_CHAT_MEMBER=0x1000, FLAG_ALL=0xFFFF,	
	OK=0, FAILED=1, ERR_NO_CLIENT=2, ERR_NO_CONNECTION=3,
	RELATION_NONE=0, RELATION_BLOCKED=1, RELATION_REQUEST_RECIPIENT=2, RELATION_FRIEND=3, RELATION_REQUEST_INITIATOR=4, RELATION_IGNORED=5, RELATION_IGNORED_FRIEND=6, RELATION_SUGGESTED=7, RELATION_MAX=8,
	AUTH_SESSION_OK=0, AUTH_SESSION_STEAM_NOT_CONNECTED=1, AUTH_SESSION_NO_LICENSE=2, AUTH_SESSION_VAC_BANNED=3, AUTH_SESSION_LOGGED_IN_ELSEWHERE=4,
	AUTH_SESSION_VAC_CHECK_TIMEOUT=5, AUTH_SESSION_TICKET_CANCELED=6, AUTH_SESSION_TICKET_ALREADY_USED=7, AUTH_SESSION_TICKET_INVALID=8, AUTH_SESSION_PUBLISHER_BANNED=9,
	AVATAR_SMALL=0, AVATAR_MEDIUM, AVATAR_LARGE,
	GLOBAL=0, GLOBAL_AROUND_USER=1, FRIENDS=2, USERS=3,
	PERSONA_NAME_MAX_UTF16=128, PERSONA_NAME_MAX_UTF8=128,
	PERSONA_CHANGE_NAME=0x0001, PERSONA_CHANGE_STATUS=0x0002, PERSONA_CHANGE_COME_ONLINE=0x0004, PERSONA_CHANGE_GONE_OFFLINE=0x0008, PERSONA_CHANGE_GAME_PLAYED=0x0010, PERSONA_CHANGE_GAME_SERVER=0x0020, PERSONA_CHANGE_AVATAR=0x0040, PERSONA_CHANGE_JOINED_SOURCE=0x0080,
	PERSONA_CHANGE_LEFT_SOURCE=0x0100, PERSONA_CHANGE_RELATIONSHIP_CHANGED=0x0200, PERSONA_CHANGE_NAME_FIRST_SET=0x0400, PERSONA_CHANGE_FACEBOOK_INFO=0x0800, PERSONA_CHANGE_NICKNAME=0x1000, PERSONA_CHANGE_STEAM_LEVEL=0x2000,
	RESTRICTION_NONE=0, RESTRICTION_UNKNOWN=1, RESTRICTION_ANY_CHAT=2, RESTRICTION_VOICE_CHAT=4, RESTRICTION_GROUP_CHAT=8, RESTRICTION_RATING=16, RESTRICTION_GAME_INVITES=32, RESTRICTION_TRADING=64,
	CHAT_INVALID=0, CHAT_MESSAGE=1, CHAT_TYPING=2, CHAT_INVITE_GAME=3, CHAT_EMOTE=4, CHAT_LEFT=6, CHAT_ENTERED=7, CHAT_KICKED=8, CHAT_BANNED=9, CHAT_DISCONNECTED=10, CHAT_HISTORICAL=11, CHAT_LINK_BLOCKED=14,
	CHAT_METADATA_MAX=8192, MAX_RICH_PRESENCE_KEYS=20, MAX_RICH_PRESENCE_KEY_LENGTH=64, MAX_RICH_PRESENCE_VALUE_LENGTH=256,
	OVERLAY_TO_STORE_FLAG_NONE=0, OVERLAY_TO_STORE_FLAG_ADD_TO_CART=1, OVERLAY_TO_STORE_FLAG_ADD_TO_CART_AND_SHOW=2,
	LOBBY_OK=0, LOBBY_NO_CONNECTION=1, LOBBY_TIMEOUT=2, LOBBY_FAIL=3, LOBBY_ACCESS_DENIED=4, LOBBY_LIMIT_EXCEEDED=5,
	PRIVATE=0, FRIENDS_ONLY=1, PUBLIC=2, INVISIBLE=3, LOBBY_KEY_LENGTH=255,
	EP2P_SEND_UNRELIABLE = 0, EP2P_SEND_UNRELIABLE_NO_DELAY = 1, EP2P_SEND_RELIABLE = 2, EP2P_SEND_RELIABLE_WITH_BUFFERING = 3,
	LOBBY_EQUAL_LESS_THAN=-2, LOBBY_LESS_THAN=-1, LOBBY_EQUAL=0, LOBBY_GREATER_THAN=1, LOBBY_EQUAL_GREATER_THAN=2, LOBBY_NOT_EQUAL=3,
	LOBBY_DISTANCE_CLOSE=0, LOBBY_DISTANCE_DEFAULT=1, LOBBY_DISTANCE_FAR=2, LOBBY_DISTANCE_WORLDWIDE=3,
	UGC_MAX_TITLE_CHARS=128, UGC_MAX_DESC_CHARS=8000, UGC_MAX_METADATA_CHARS=5000,
	UGC_ITEM_COMMUNITY=0, UGC_ITEM_MICROTRANSACTION=1, UGC_ITEM_COLLECTION=2, UGC_ITEM_ART=3, UGC_ITEM_VIDEO=4, UGC_ITEM_SCREENSHOT=5, UGC_ITEM_GAME=6, UGC_ITEM_SOFTWARE=7,
	UGC_ITEM_CONCEPT=8, UGC_ITEM_WEBGUIDE=9, UGC_ITEM_INTEGRATEDGUIDE=10, UGC_ITEM_MERCH=11, UGC_ITEM_CONTROLLERBINDING=12, UGC_ITEM_STEAMWORKSACCESSINVITE=13,
	UGC_ITEM_STEAMVIDEO=14, UGC_ITEM_GAMEMANAGEDITEM=15, UGC_ITEM_MAX=16,
	UGC_STATE_NONE=0, UGC_STATE_SUBSCRIBED=1, UGC_STATE_LEGACY=2, UGC_STATE_INSTALLED=4, UGC_STATE_UPDATE=8, UGC_STATE_DOWNLOADING=16, UGC_STATE_PENDING=32,
	UGC_FILE_VISIBLE_PUBLIC=0, UGC_FILE_VISIBLE_FRIENDS=1, UGC_FILE_VISIBLE_PRIVATE=2,
	STATUS_INVALID=0, STATUS_PREPARING_CONFIG=1, STATUS_PREPARING_CONTENT=2, STATUS_UPLOADING_CONTENT=3, STATUS_UPLOADING_PREVIEW=4, STATUS_COMMITTING_CHANGES=5,
	REMOTE_STORAGE_PLATFORM_NONE=0, REMOTE_STORAGE_PLATFORM_WINDOWS=(1<<0), REMOTE_STORAGE_PLATFORM_OSX=(1<<1), REMOTE_STORAGE_PLATFORM_PS3=(1<<2), 
	REMOTE_STORAGE_PLATFORM_LINUX=(1<<3), REMOTE_STORAGE_PLATFORM_RESERVED2=(1<<4), REMOTE_STORAGE_PLATFORM_ALL=0xffffffff,
	RESULT_OK=1, RESULT_FAIL=2, RESULT_NO_CONNECT=3, RESULT_INVALID_PASSWORD=5, RESULT_LOGGED_IN_ESLEWHERE=6, RESULT_INVALID_PROTOCAL=7, RESULT_INALID_PARAM=8, RESULT_FILE_NOT_FOUND=9, RESULT_BUSY=10, RESULT_INVALID_STATE=11, RESULT_INVALID_NAME=12,
	RESULT_INVALID_EMAIL=13, RESULT_DUPLICATE_NAME=14, RESULT_ACCESS_DENIED=15, RESULT_TIMEOUT=16, RESULT_BANNED=17, RESULT_ACCOUNT_NOT_FOUND=18, RESULT_INVALID_STEAM_ID=19, RESULT_SERVICE_UNAVAILABLE=20, RESULT_NOT_LOGGED_ON=21, RESULT_PENDING=22,
	RESULT_ENCRYPT_FAILURE=23, RESULT_INSUFFICIENT_PRIVILEGE=24, RESULT_LIMIT_EXCEEDED=25, RESULT_REVOKED=26, RESULT_EXPIRED=27, RESULT_ALREADY_REDEEMED=28, RESULT_DUPLICATE_REQUEST=29, RESULT_ALREADY_OWNED=30, RESULT_IP_NOT_FOUND=31, RESULT_PERSIST_FAILED=32,
	RESULT_LOCKING_FAILED=33, RESULT_LOGON_SESSION_REPLACED=34, RESULT_CONNECT_FAILED=35, RESULT_HANDSHAKE_FAILED=36, RESULT_IO_FAILURE=37, RESULT_REMOTE_DISCONNECT=38, RESULT_SHOPPING_CART_NOT_FOUND=39, RESULT_BLOCKED=40, RESULT_IGNORED=41, RESULT_NO_MATCH=42,
	RESULT_ACCOUNT_DISABLED=43, RESULT_SERVICE_READY_ONLY=44, RESULT_ACCOUNT_NOT_FEATURED=45, RESULT_ADMINISTRATOR_OK=46, RESULT_CONTENT_VERSION=47, RESULT_TRY_ANOTHER_CM=48, RESULT_PASSWORD_REQUIRED_TO_KICK=49, RESULT_ALREADY_LOGGED_ELSEWHERE=50,
	RESULT_SUSPENDED=51, RESULT_CANCELLED=52, RESULT_DATA_CORRUPTION=53, RESULT_DISK_FULL=54, RESULT_REMOTE_CALL_FAILED=55, RESULT_PASSWORD_UNSET=56, RESULT_EXTERNAL_ACCOUNT_UNLINKED=57, RESULT_PSN_TICKET_INVALID=58, RESULT_EXTERNAL_ACCOUNT_ALREADY_LINKED=59,
	RESULT_REMOTE_FILE_CONFLICT=60, RESULT_ILLEGAL_PASSWORD=61, RESULT_SAME_AS_PREVIOUS_VALUE=62, RESULT_ACCOUNT_LOGON_DENIED=63, RESULT_CANNOT_USE_OLD_PASSWORD=64, RESULT_INVALID_LOGIN_AUTH_CODE=65, RESULT_ACCOUNT_LOGON_DENIED_NO_MAIL=66, RESULT_HARDWARE_NOT_CAPABLE=67,
	RESULT_IP_INIT_ERROR=68, RESULT_PARENTAL_CONTROL_RESTRICTED=69, RESULT_FACEBOOK_QUERY_ERROR=70, RESULT_EXPIRED_LOGIN_AUTH_CODE=71, RESULT_IP_LOGIN_RESTRICTION_FAILED=72, RESULT_ACCOUNT_LOCKED_DOWN=73, RESULT_ACCOUNT_LOGON_DENIED_VERIFIED_EMAIL_REQUIRED=74,
	RESULT_NO_MATCHING_URL=75, RESULT_BAD_RESPONSE=76, RESULT_REQUIRED_PASSWORD_REENTRY=77, RESULT_VALUE_OUT_OF_RANGE=78, RESULT_UNEXPECTED_ERROR=79, RESULT_DISABLED=80, RESULT_INVALID_CEG_SUBMISSION=81, RESULT_RESTRICTED_DEVICE=82, RESULT_REGION_LOCKED=83,
	RESULT_RATE_LIMIT_EXCEEDED=84, RESULT_ACCOUNT_LOGIN_DENIED_NEED_TWO_FACTOR=85, RESULT_ITEM_DELETED=86, RESULT_ACCOUNT_LOGIN_DENIED_THROTTLE=87, RESULT_TWO_FACTOR_CODE_MISMATCH=88, RESULT_TWO_FACTOR_ACTIVATION_CODE_MISMATCH=89, RESULT_ACCOUNT_ASSOCIATED_TO_MULTIPLE_PARTNERS=90,
	RESULT_NOT_MODIFIED=91, RESULT_NO_MOBILE_DEVICE=92, RESULT_TIME_NOT_SYNCED=93, RESULT_SMS_CODE_FAILED=94, RESULT_ACCOUNT_LIMIT_EXCEEDED=95, RESULT_ACCOUNT_ACTIVITY_LIMIT_EXCEEDED=96, RESULT_PHONE_ACTIVITY_LIMIT_EXCEEDED=97, RESULT_REFUND_TO_WALLET=98,
	RESULT_EMAIL_SEND_FAILURE=99, RESULT_NOT_SETTLED=100, RESULT_NEED_CAPTCHA=101, RESULT_GSLT_DENIED=102, RESULT_GS_OWNER_DENIED=103,RESULT_INVALID_ITEM_TYPE=104, RESULT_IP_BANNED=105, RESULT_GSLT_EXPIRED=106, RESULT_INSUFFICIENT_FUNDS=107, RESULT_TOO_MANY_PENDING=108,
	CHAT_ROOM_SUCCESS=1, CHAT_ROOM_DOESNT_EXIST=2, CHAT_ROOM_NOT_ALLOWED=3, CHAT_ROOM_FULL=4, CHAT_ROOM_ERROR=5, CHAT_ROOM_BANNED=6, CHAT_ROOM_LIMITED=7, CHAT_ROOM_CLAN_DISABLED=8, CHAT_ROOM_COMMUNITY_BAN=9, CHAT_ROOM_MEMBER_BLOCKED_YOU=10, CHAT_ROOM_YOU_BLOCKED_MEMBER=11,
	GAMEID_TYPE_APP=0, GAMEID_TYPE_MOD=1, GAMEID_TYPE_SHORTCUT=2, GAMEID_TYPE_P2P=3,
	FAVORITE_FLAG_FAVORITE=0x01, FAVORITE_FLAG_HISTORY=0x02, FAVORITE_FLAG_NONE=0x00,
	CHAT_MEMBER_CHANGE_ENTERED=0x0001, CHAT_MEMBER_CHANGE_LEFT=0x0002, CHAT_MEMBER_CHANGE_DISCONNECTED=0x0004, CHAT_MEMBER_CHANGE_KICKED=0x0008, CHAT_MEMBER_CHANGE_BANNED=0x0010,
	FAILURE_FLUSHED_CALLBACK_QUEUE=0, FAILURE_PIPE_FAIL=1,
	GAMEPAD_INPUT_LINE_MODE_SINGLE=0, GAMEPAD_INPUT_LINE_MODE_MULTIPLE=1,
	GAMEPAD_INPUT_MODE_NORMAL=0, GAMEPAD_INPUT_MODE_PASSWORD=1,
	STEAM_API_CALL_FAILURE_NONE=-1, STEAM_API_CALL_FAILURE_STEAM_GONE=0, STEAM_API_CALL_FAILURE_NETWORK_FAILURE=1, STEAM_API_CALL_FAILURE_INVALID_HANDLE=2, STEAM_API_CALL_FAILURE_MISMATCHED_CALLBACK=3
};

/////////////////////////////////////////////////
///// MAIN FUNCTIONS ////////////////////////////
/////////////////////////////////////////////////
//
// Checks if your executable was launched through Steam and relaunches it through Steam if it wasn't.
SW_PY bool RestartAppIfNecessary(int value){
	return SteamAPI_RestartAppIfNecessary((AppId_t)value);
}
// Initialize Steamworks
SW_PY int SteamInit(){
	// Attempt to initialize Steamworks
	bool isInitSuccess = SteamAPI_Init();
	// Set the default status response
	int status = FAILED;
	// Steamworks initialized with no problems
	if(isInitSuccess){
		status = OK;
	}
	// The Steam client is not running
	if(!SteamAPI_IsSteamRunning()){
		status = ERR_NO_CLIENT;
	}
	// The user is not logged into Steam or there is no active connection to Steam
	else if(!SteamUser()->BLoggedOn()){
		status = ERR_NO_CONNECTION;
	}
	// Steam is connected and active, so load the stats and achievements
	if(status == OK && SteamUserStats() != NULL){
		SteamUserStats()->RequestCurrentStats();
	}
	// Return the Steamworks status
	return status;
}
// Returns true/false if Steam is running.
SW_PY bool IsSteamRunning(void){
	return SteamAPI_IsSteamRunning();
}

/////////////////////////////////////////////////
///// APPS //////////////////////////////////////
/////////////////////////////////////////////////
//
// Checks if the active user is subscribed to the current App ID.
SW_PY bool IsSubscribed(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribed();
}
// Checks if the license owned by the user provides low violence depots.
SW_PY bool IsLowViolence(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsLowViolence();
}
// Checks whether the current App ID is for Cyber Cafes.
SW_PY bool IsCybercafe(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsCybercafe();
}
// Checks if the user has a VAC ban on their account.
SW_PY bool IsVACBanned(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsVACBanned();
}
// Gets the current language that the user has set.
SW_PY const char* GetCurrentGameLanguage(){
	if(SteamApps() == NULL){
		return "None";
	}
	return SteamApps()->GetCurrentGameLanguage();
}
// Gets a comma separated list of the languages the current app supports.
SW_PY const char* GetAvailableGameLanguages(){
	if(SteamApps() == NULL){
		return "None";
	}
	return SteamApps()->GetAvailableGameLanguages();
}
// Checks if the active user is subscribed to a specified AppId.
SW_PY bool IsSubscribedApp(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribedApp((AppId_t)value);
}
// Checks if the user owns a specific DLC and if the DLC is installed
SW_PY bool IsDLCInstalled(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsDlcInstalled(value);
}
// Gets the time of purchase of the specified app in Unix epoch format (time since Jan 1st, 1970).
SW_PY int GetEarliestPurchaseUnixTime(int value){
	if(SteamApps() == NULL){
		return 0;
	}
	return SteamApps()->GetEarliestPurchaseUnixTime((AppId_t)value);
}
// Checks if the user is subscribed to the current app through a free weekend.
// This function will return false for users who have a retail or other type of license.
// Suggested you contact Valve on how to package and secure your free weekend properly.
SW_PY bool IsSubscribedFromFreeWeekend(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribedFromFreeWeekend();
}
// Get the number of DLC the user owns for a parent application/game.
SW_PY int GetDLCCount(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->GetDLCCount();
}
// Allows you to install an optional DLC.
SW_PY void InstallDLC(int value){
	if(SteamApps() == NULL){
		return;
	}
	SteamApps()->InstallDLC((AppId_t)value);
}
// Allows you to uninstall an optional DLC.
SW_PY void UninstallDLC(int value){
	if(SteamApps() == NULL){
		return;
	}
	SteamApps()->UninstallDLC((AppId_t)value);
}
// Allows you to force verify game content on next launch.
SW_PY bool MarkContentCorrupt(bool missingFilesOnly){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->MarkContentCorrupt(missingFilesOnly);
}
// Gets the install folder for a specific AppID.
SW_PY const char* GetAppInstallDir(AppId_t appID){
	if(SteamApps() == NULL){
		return "";
	}
	const uint32 folderBuffer = 256;
	char *buffer = new char[folderBuffer];
	SteamApps()->GetAppInstallDir(appID, (char*)buffer, folderBuffer);
	const char* appDir = buffer;
	delete buffer;
	return appDir;
}
// Check if given application/game is installed, not necessarily owned.
SW_PY bool IsAppInstalled(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsAppInstalled((AppId_t)value);
}
// Gets the Steam ID of the original owner of the current app. If it's different from the current user then it is borrowed.
SW_PY uint64_t GetAppOwner(){
	if(SteamApps() == NULL){
		return 0;
	}
	CSteamID cSteamID = SteamApps()->GetAppOwner();
	return cSteamID.ConvertToUint64();
}
// Gets the associated launch parameter if the game is run via steam://run/<appid>/?param1=value1;param2=value2;param3=value3 etc.
SW_PY const char* GetLaunchQueryParam(const char* key){
	if(SteamApps() == NULL){
		return "";
	}
	return SteamApps()->GetLaunchQueryParam(key);
}
// Return the build ID for this app; will change based on backend updates.
SW_PY int GetAppBuildId(){
	if(SteamApps() == NULL){
		return 0;
	}
	return SteamApps()->GetAppBuildId();
}
// Asynchronously retrieves metadata details about a specific file in the depot manifest.
SW_PY void GetFileDetails(const char* filename){
	if(SteamApps() == NULL){
		return;
	}
	SteamApps()->GetFileDetails(filename);
}

/////////////////////////////////////////////////
///// MUSIC /////////////////////////////////////
/////////////////////////////////////////////////
//
// Is Steam music enabled.
SW_PY bool MusicIsEnabled(){
	if(SteamMusic() == NULL){
		return false;
	}
	return SteamMusic()->BIsEnabled();
}
// Is Steam music playing something.
SW_PY bool MusicIsPlaying(){
	if(SteamMusic() == NULL){
		return false;
	}
	return SteamMusic()->BIsPlaying();
}
// Get the volume level of the music.
SW_PY float MusicGetVolume(){
	if(SteamMusic() == NULL){
		return 0;
	}
	return SteamMusic()->GetVolume();
}
// Pause whatever Steam music is playing.
SW_PY void MusicPause(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->Pause();
}
// Play current track/album.
SW_PY void MusicPlay(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->Play();
}
// Play next track/album.
SW_PY void MusicPlayNext(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->PlayNext();
}
// Play previous track/album.
SW_PY void MusicPlayPrev(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->PlayPrevious();
}
// Set the volume of Steam music.
SW_PY void MusicSetVolume(float value){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->SetVolume(value);
}

/////////////////////////////////////////////////
///// SCREENSHOTS ///////////////////////////////
/////////////////////////////////////////////////
//
// Adds a screenshot to the user's Steam screenshot library from disk.
SW_PY uint32_t AddScreenshotToLibrary(const char* filename, const char* thumbnailFilename, int width, int height){
	if(SteamScreenshots() == NULL){
		return 0;
	}
	return SteamScreenshots()->AddScreenshotToLibrary(filename, thumbnailFilename, width, height);
}
// Toggles whether the overlay handles screenshots.
SW_PY void HookScreenshots(bool hook){
	if(SteamScreenshots() == NULL){
		return;
	}
	SteamScreenshots()->HookScreenshots(hook);
}
// Checks if the app is hooking screenshots.
SW_PY bool IsScreenshotsHooked(){
	if(SteamScreenshots() == NULL){
		return false;
	}
	return SteamScreenshots()->IsScreenshotsHooked();
}
// Sets optional metadata about a screenshot's location.
SW_PY bool SetLocation(uint32_t screenshot, const char* location){
	if(SteamScreenshots() == NULL){
		return false;
	}
	ScreenshotHandle handle = (ScreenshotHandle)screenshot;
	return SteamScreenshots()->SetLocation(handle, location);
}
// Causes Steam overlay to take a screenshot.
SW_PY void TriggerScreenshot(){
	if(SteamScreenshots() == NULL){
		return;
	}
	SteamScreenshots()->TriggerScreenshot();
}

/////////////////////////////////////////////////
///// USERS /////////////////////////////////////
/////////////////////////////////////////////////
//
// Get user's Steam ID.
SW_PY uint64_t GetSteamID(){
	if(SteamUser() == NULL){
		return 0;
	}
	CSteamID steamID = SteamUser()->GetSteamID();
	return steamID.ConvertToUint64();
}
// Check, true/false, if user is logged into Steam currently.
SW_PY bool LoggedOn(){
	if(SteamUser() == NULL){
		return false;
	}
	return SteamUser()->BLoggedOn();
}
// Get the user's Steam level.
SW_PY int GetPlayerSteamLevel(){
	if(SteamUser() == NULL){
		return 0;
	}
	return SteamUser()->GetPlayerSteamLevel(); 
}
// Get the user's Steam installation path (this function is depreciated).
SW_PY const char* GetUserDataFolder(){
	if(SteamUser() == NULL){
		return "";
	}
	const int bufferSize = 256;
	char *buffer = new char[bufferSize];
	SteamUser()->GetUserDataFolder((char*)buffer, bufferSize);
	char *data_path = buffer;
	delete buffer;
	return data_path;
}
// Trading Card badges data access, if you only have one set of cards, the series will be 1.
// The user has can have two different badges for a series; the regular (max level 5) and the foil (max level 1).
SW_PY int GetGameBadgeLevel(int series, bool foil){
	if(SteamUser()== NULL){
		return 0;
	}
	return SteamUser()->GetGameBadgeLevel(series, foil);
}

/////////////////////////////////////////////////
///// UTILS /////////////////////////////////////
/////////////////////////////////////////////////
//
// Checks if the Overlay needs a present. Only required if using event driven render updates.
SW_PY bool OverlayNeedsPresent(){
	if(SteamUtils() == NULL){
		return false;
	}
	return SteamUtils()->BOverlayNeedsPresent();
}
// Get the Steam ID of the running application/game.
SW_PY int GetAppID(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetAppID();
}
// Get the amount of battery power, clearly for laptops.
SW_PY int GetCurrentBatteryPower(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetCurrentBatteryPower();
}
// Returns the number of IPC calls made since the last time this function was called.
SW_PY uint32 GetIPCCallCount(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetIPCCallCount();
}
// Get the user's country by IP.
SW_PY const char* GetIPCountry(){
	if(SteamUtils() == NULL){
		return "";
	}
	return SteamUtils()->GetIPCountry();
}
// Return amount of time, in seconds, user has spent in this session.
SW_PY int GetSecondsSinceAppActive(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetSecondsSinceAppActive();
}
// Returns the number of seconds since the user last moved the mouse.
SW_PY int GetSecondsSinceComputerActive(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetSecondsSinceComputerActive();
}
// Get the actual time.
SW_PY int GetServerRealTime(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetServerRealTime();
}
// Get the Steam user interface language.
SW_PY const char* GetSteamUILanguage(){
	if(SteamUtils() == NULL){
		return "";
	}
	return SteamUtils()->GetSteamUILanguage();
}
// Returns true/false if Steam overlay is enabled.
SW_PY bool IsOverlayEnabled(){
	if(SteamUtils() == NULL){
		return false;
	}
	return SteamUtils()->IsOverlayEnabled();
}
// Returns true if Steam & the Steam Overlay are running in Big Picture mode.
SW_PY bool IsSteamInBigPictureMode(){
	if(SteamUtils() == NULL){
		return false;
	}
	return SteamUtils()->IsSteamInBigPictureMode();
}
// Is Steam running in VR?
SW_PY bool IsSteamRunningInVR(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->IsSteamRunningInVR();
}
// Checks if the HMD view will be streamed via Steam In-Home Streaming.
SW_PY bool IsVRHeadsetStreamingEnabled(){
	if(SteamUtils() == NULL){
		return false;
	}
	return SteamUtils()->IsVRHeadsetStreamingEnabled();	
}
// Sets the inset of the overlay notification from the corner specified by SetOverlayNotificationPosition.
SW_PY void SetOverlayNotificationInset(int horizontal, int vertical){
	if(SteamUtils() == NULL){
		return;
	}
	SteamUtils()->SetOverlayNotificationInset(horizontal, vertical);
}
// Set the position where overlay shows notifications.
SW_PY void SetOverlayNotificationPosition(int pos){
	if((pos < 0) || (pos > 3) || (SteamUtils() == NULL)){
		return;
	}
	SteamUtils()->SetOverlayNotificationPosition(ENotificationPosition(pos));
}
// Set whether the HMD content will be streamed via Steam In-Home Streaming.
SW_PY void SetVRHeadsetStreamingEnabled(bool enabled){
	if(SteamUtils() == NULL){
		return;
	}
	SteamUtils()->SetVRHeadsetStreamingEnabled(enabled);
}
// Activates the Big Picture text input dialog which only supports gamepad input.
SW_PY bool ShowGamepadTextInput(int inputMode, int lineInputMode, const char* description, uint32 maxText, const char* presetText){
	if(SteamUtils() == NULL){
		return false;
	}
	// Convert modes
	EGamepadTextInputMode mode;
	if(inputMode == 0){
		mode = k_EGamepadTextInputModeNormal;
	}
	else{
		mode = k_EGamepadTextInputModePassword;
	}
	EGamepadTextInputLineMode lineMode;
	if(lineInputMode == 0){
		lineMode = k_EGamepadTextInputLineModeSingleLine;
	}
	else{
		lineMode = k_EGamepadTextInputLineModeMultipleLines;
	}
	return SteamUtils()->ShowGamepadTextInput(mode, lineMode, description, maxText, presetText);
}
// Ask SteamUI to create and render its OpenVR dashboard.
SW_PY void StartVRDashboard(){
	if(SteamUtils() == NULL){
		return;
	}
	SteamUtils()->StartVRDashboard();
}