/////////////////////////////////////////////////
//  STEAMWORKSPY - STEAMWORKS FOR PYTHON
/////////////////////////////////////////////////
//
// Modify SW_PY based on operating system and include the proper Steamworks API file
//
// Include the Steamworks API header
#if defined( _WIN32 )
#include "sdk\steam\steam_api.h"
#define SW_PY extern "C" __declspec(dllexport)
#elif defined( __APPLE__ )
#include "sdk/steam/steam_api.h"
#include "TargetConditionals.h"
#define SW_PY extern "C" __attribute__ ((visibility("default")))
#elif defined( __linux__ )
#include "sdk/steam/steam_api.h"
#define SW_PY extern "C" __attribute__ ((visibility("default")))
#else
#error "Unsupported platform"
#endif

#include <iostream>
#include <string>

//-----------------------------------------------
// Definitions
//-----------------------------------------------
//#define IS_INIT_SUCCESS
#define IS_VALID
#define OFFLINE 0
#define ONLINE 1
#define BUSY 2
#define AWAY 3
#define SNOOZE 4
#define LF_TRADE
#define LF_PLAY
#define STATE_MAX
#define NOT_OFFLINE 8
#define ALL 9
#define TOP_LEFT 0
#define TOP_RIGHT 1
#define BOT_LEFT 2
#define BOT_RIGHT 3
#define OK 0
#define FAILED 1
#define ERR_NO_CLIENT 2
#define ERR_NO_CONNECTION 3
#define AVATAR_SMALL 0
#define AVATAR_MEDIUM 1
#define AVATAR_LARGE 2
#define GLOBAL 0
#define GLOBAL_AROUND_USER 1
#define FRIENDS 2
#define USERS 3
#define LOBBY_OK 0
#define LOBBY_NO_CONNECTION 1
#define LOBBY_TIMEOUT 2
#define LOBBY_FAIL 3
#define LOBBY_ACCESS_DENIED 4
#define LOBBY_LIMIT_EXCEEDED 5
#define PRIVATE 0
#define FRIENDS_ONLY 1
#define PUBLIC 2
#define INVISIBLE 3
#define LOBBY_KEY_LENGTH 255
#define UGC_MAX_TITLE_CHARS 128
#define UGC_MAX_DESC_CHARS 8000
#define UGC_MAX_METADATA_CHARS 5000
#define UGC_ITEM_COMMUNITY 0
#define UGC_ITEM_MICROTRANSACTION 1
#define UGC_STATE_NONE 0
#define UGC_STATE_SUBSCRIBED 1
#define UGC_STATE_LEGACY 2
#define UGC_STATE_INSTALLED 4
#define UGC_STATE_UPDATE 8
#define UGC_STATE_DOWNLOADING 16
#define UGC_STATE_PENDING 32
#define STATUS_INVALID 0
#define STATUS_PREPARING_CONFIG 1
#define STATUS_PREPARING_CONTENT 2
#define STATUS_UPLOADING_CONTENT 3
#define STATUS_UPLOADING_PREVIEW 4
#define STATUS_COMMITTING_CHANGES 5
typedef void(*CreateItemResultCallback_t)(CreateItemResult_t);
typedef void(*SubmitItemUpdateResultCallback_t)(SubmitItemUpdateResult_t);
typedef void(*ItemInstalledCallback_t)(ItemInstalled_t);

struct SubscriptionResult {
	std::int32_t result;
	std::uint64_t publishedFileId;
};

typedef void(*RemoteStorageSubscribeFileResultCallback_t)(SubscriptionResult);
typedef void(*RemoteStorageUnsubscribeFileResultCallback_t)(SubscriptionResult);
typedef void(*LeaderboardFindResultCallback_t)(LeaderboardFindResult_t);
typedef void(*MicroTxnAuthorizationResponseCallback_t)(MicroTxnAuthorizationResponse_t);

//-----------------------------------------------
// Workshop Class
//-----------------------------------------------
class Workshop {
public:
    CreateItemResultCallback_t _pyItemCreatedCallback;
    SubmitItemUpdateResultCallback_t _pyItemUpdatedCallback;
    ItemInstalledCallback_t _pyItemInstalledCallback;
    RemoteStorageSubscribeFileResultCallback_t _pyItemSubscribedCallback;
    RemoteStorageUnsubscribeFileResultCallback_t _pyItemUnsubscribedCallback;

    CCallResult <Workshop, CreateItemResult_t> _itemCreatedCallback;
    CCallResult <Workshop, SubmitItemUpdateResult_t> _itemUpdatedCallback;
    CCallResult <Workshop, RemoteStorageSubscribePublishedFileResult_t> _itemSubscribedCallback;
    CCallResult <Workshop, RemoteStorageUnsubscribePublishedFileResult_t> _itemUnsubscribedCallback;

    CCallback <Workshop, ItemInstalled_t> _itemInstalledCallback;

    Workshop() : _itemInstalledCallback(this, &Workshop::OnItemInstalled) {}

    void SetItemCreatedCallback(CreateItemResultCallback_t callback) {
        _pyItemCreatedCallback = callback;
    }

    void SetItemUpdatedCallback(SubmitItemUpdateResultCallback_t callback) {
        _pyItemUpdatedCallback = callback;
    }

    void SetItemInstalledCallback(ItemInstalledCallback_t callback) {
        _pyItemInstalledCallback = callback;
    }

    void ClearItemInstallCallback() {
        _pyItemInstalledCallback = nullptr;
    }

    void SetItemSubscribedCallback(RemoteStorageSubscribeFileResultCallback_t callback) {
        _pyItemSubscribedCallback = callback;
    }

    void SetItemUnsubscribedCallback(RemoteStorageUnsubscribeFileResultCallback_t callback) {
        _pyItemUnsubscribedCallback = callback;
    }

    void CreateItem(AppId_t consumerAppId, EWorkshopFileType fileType) {
        //TODO: Check if fileType is a valid value?
        SteamAPICall_t createItemCall = SteamUGC()->CreateItem(consumerAppId, fileType);
        _itemCreatedCallback.Set(createItemCall, this, &Workshop::OnWorkshopItemCreated);
    }

    void SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *pChangeNote) {
        SteamAPICall_t submitItemUpdateCall = SteamUGC()->SubmitItemUpdate(updateHandle, pChangeNote);
        _itemUpdatedCallback.Set(submitItemUpdateCall, this, &Workshop::OnItemUpdateSubmitted);
    }

    void SubscribeItem(PublishedFileId_t publishedFileID) {
        SteamAPICall_t subscribeItemCall = SteamUGC()->SubscribeItem(publishedFileID);
        _itemSubscribedCallback.Set(subscribeItemCall, this, &Workshop::OnItemSubscribed);
    }

    void UnsubscribeItem(PublishedFileId_t publishedFileID) {
        SteamAPICall_t unsubscribeItemCall = SteamUGC()->UnsubscribeItem(publishedFileID);
        _itemUnsubscribedCallback.Set(unsubscribeItemCall, this, &Workshop::OnItemUnsubscribed);
    }

private:
    void OnWorkshopItemCreated(CreateItemResult_t *createItemResult, bool bIOFailure) {
        if (_pyItemCreatedCallback != nullptr) {
            _pyItemCreatedCallback(*createItemResult);
        }
    }

    void OnItemUpdateSubmitted(SubmitItemUpdateResult_t *submitItemUpdateResult, bool bIOFailure) {
        if (_pyItemUpdatedCallback != nullptr) {
            _pyItemUpdatedCallback(*submitItemUpdateResult);
        }
    }

    void OnItemInstalled(ItemInstalled_t *itemInstalledResult) {
        if (_pyItemInstalledCallback != nullptr) {
            _pyItemInstalledCallback(*itemInstalledResult);
        }
    }

    void OnItemSubscribed(RemoteStorageSubscribePublishedFileResult_t *itemSubscribedResult, bool bIOFailure) {
        if (_pyItemSubscribedCallback != nullptr) {
            SubscriptionResult result{itemSubscribedResult->m_eResult, itemSubscribedResult->m_nPublishedFileId};
            _pyItemSubscribedCallback(result);
        }
    }

    void OnItemUnsubscribed(RemoteStorageUnsubscribePublishedFileResult_t *itemUnsubscribedResult, bool bIOFailure) {
        if (_pyItemUnsubscribedCallback != nullptr) {
            SubscriptionResult result{itemUnsubscribedResult->m_eResult, itemUnsubscribedResult->m_nPublishedFileId};
            _pyItemUnsubscribedCallback(result);
        }
    }
};

static Workshop workshop;

//-----------------------------------------------
// Leaderboard Class
//-----------------------------------------------
class Leaderboard {
public:
    LeaderboardFindResultCallback_t _pyLeaderboardFindResultCallback;

    CCallResult <Leaderboard, LeaderboardFindResult_t> _leaderboardFindResultCallback;

    void SetLeaderboardFindResultCallback(LeaderboardFindResultCallback_t callback) {
        _pyLeaderboardFindResultCallback = callback;
    }

    void FindLeaderboard(const char *pchLeaderboardName) {
        SteamAPICall_t leaderboardFindResultCall = SteamUserStats()->FindLeaderboard(pchLeaderboardName);
        _leaderboardFindResultCallback.Set(leaderboardFindResultCall, this, &Leaderboard::OnLeaderboardFindResult);
    }

private:
    void OnLeaderboardFindResult(LeaderboardFindResult_t *leaderboardFindResult, bool bIOFailure) {
        if (_pyLeaderboardFindResultCallback != nullptr) {
            _pyLeaderboardFindResultCallback(*leaderboardFindResult);
        }
    }
};

static Leaderboard leaderboard;

//-----------------------------------------------
// MicroTxn Class
//-----------------------------------------------
class MicroTxn {
public:
    MicroTxnAuthorizationResponseCallback_t _pyMicroTxnAuthorizationResponseCallback;

    CCallback <MicroTxn, MicroTxnAuthorizationResponse_t> _microTxnAuthorizationResponseCallback;

    MicroTxn() : _microTxnAuthorizationResponseCallback(this, &MicroTxn::OnAuthorizationResponse) {}

    void SetAuthorizationResponseCallback(MicroTxnAuthorizationResponseCallback_t callback) {
        _pyMicroTxnAuthorizationResponseCallback = callback;
    }

private:
    void OnAuthorizationResponse(MicroTxnAuthorizationResponse_t *authorizationResponse) {
        if (_pyMicroTxnAuthorizationResponseCallback != nullptr) {
            _pyMicroTxnAuthorizationResponseCallback(*authorizationResponse);
        }
    }
};

static MicroTxn microtxn;

/////////////////////////////////////////////////
///// MAIN FUNCTIONS ////////////////////////////
/////////////////////////////////////////////////
//
// Checks if your executable was launched through Steam and relaunches it through Steam if it wasn't.
SW_PY bool RestartAppIfNecessary(int value) {
    return SteamAPI_RestartAppIfNecessary((AppId_t) value);
}

// Initialize Steamworks
SW_PY int SteamInit() {
    // Attempt to initialize Steamworks
    bool isInitSuccess = SteamAPI_Init();
    // Set the default status response
    int status = FAILED;
    // Steamworks initialized with no problems
    if (isInitSuccess) {
        status = OK;
    }
    // The Steam client is not running
    if (!SteamAPI_IsSteamRunning()) {
        status = ERR_NO_CLIENT;
    }
        // The user is not logged into Steam or there is no active connection to Steam
    else if (!SteamUser()->BLoggedOn()) {
        status = ERR_NO_CONNECTION;
    }
    // Steam is connected and active, so load the stats and achievements
    if (status == OK && SteamUserStats() != NULL) {
        SteamUserStats()->RequestCurrentStats();
    }
    // Return the Steamworks status
    return status;
}

// Returns true/false if Steam is running
SW_PY bool IsSteamRunning(void) {
    return SteamAPI_IsSteamRunning();
}

// Create a Steam ID
CSteamID CreateSteamID(uint32 steamID, int accountType) {
    CSteamID cSteamID;
    if (accountType < 0 || accountType >= k_EAccountTypeMax) {
        accountType = 1;
    }
    cSteamID.Set(steamID, EUniverse(k_EUniversePublic), EAccountType(accountType));
    return cSteamID;
}

// Callbacks
SW_PY void RunCallbacks() {
    SteamAPI_RunCallbacks();
}

// Shuts down the Steamworks API, releases pointers and frees memory.
SW_PY void SteamShutdown() {
    SteamAPI_Shutdown();
}

/////////////////////////////////////////////////
///// APPS //////////////////////////////////////
/////////////////////////////////////////////////
//
// Checks if the active user is subscribed to the current App ID.
SW_PY bool IsSubscribed() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsSubscribed();
}

// Checks if the license owned by the user provides low violence depots.
SW_PY bool IsLowViolence() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsLowViolence();
}

// Checks whether the current App ID is for Cyber Cafes.
SW_PY bool IsCybercafe() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsCybercafe();
}

// Checks if the user has a VAC ban on their account.
SW_PY bool IsVACBanned() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsVACBanned();
}

// Gets the current language that the user has set.
SW_PY const char *GetCurrentGameLanguage() {
    if (SteamApps() == NULL) {
        return "None";
    }
    return SteamApps()->GetCurrentGameLanguage();
}

// Gets a comma separated list of the languages the current app supports.
SW_PY const char *GetAvailableGameLanguages() {
    if (SteamApps() == NULL) {
        return "None";
    }
    return SteamApps()->GetAvailableGameLanguages();
}

// Checks if the active user is subscribed to a specified AppId.
SW_PY bool IsSubscribedApp(int value) {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsSubscribedApp((AppId_t) value);
}

// Checks if the user owns a specific DLC and if the DLC is installed
SW_PY bool IsDLCInstalled(int value) {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsDlcInstalled(value);
}

// Gets the time of purchase of the specified app in Unix epoch format (time since Jan 1st, 1970).
SW_PY int GetEarliestPurchaseUnixTime(int value) {
    if (SteamApps() == NULL) {
        return 0;
    }
    return SteamApps()->GetEarliestPurchaseUnixTime((AppId_t) value);
}

// Checks if the user is subscribed to the current app through a free weekend.
// This function will return false for users who have a retail or other type of license.
// Suggested you contact Valve on how to package and secure your free weekend properly.
SW_PY bool IsSubscribedFromFreeWeekend() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsSubscribedFromFreeWeekend();
}

// Get the number of DLC the user owns for a parent application/game.
SW_PY int GetDLCCount() {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->GetDLCCount();
}

// Allows you to install an optional DLC.
SW_PY void InstallDLC(int value) {
    if (SteamApps() == NULL) {
        return;
    }
    SteamApps()->InstallDLC((AppId_t) value);
}

// Allows you to uninstall an optional DLC.
SW_PY void UninstallDLC(int value) {
    if (SteamApps() == NULL) {
        return;
    }
    SteamApps()->UninstallDLC((AppId_t) value);
}

// Allows you to force verify game content on next launch.
SW_PY bool MarkContentCorrupt(bool missingFilesOnly) {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->MarkContentCorrupt(missingFilesOnly);
}

// Gets the install folder for a specific AppID.
SW_PY const char *GetAppInstallDir(AppId_t appID) {
    if (SteamApps() == NULL) {
        return "";
    }
    const uint32 folderBuffer = 256;
    char *buffer = new char[folderBuffer];
    SteamApps()->GetAppInstallDir(appID, (char *) buffer, folderBuffer);
    const char *appDir = buffer;
    delete buffer;
    return appDir;
}

// Check if given application/game is installed, not necessarily owned.
SW_PY bool IsAppInstalled(int value) {
    if (SteamApps() == NULL) {
        return false;
    }
    return SteamApps()->BIsAppInstalled((AppId_t) value);
}

// Gets the Steam ID of the original owner of the current app. If it's different from the current user then it is borrowed.
SW_PY uint64_t

GetAppOwner() {
    if (SteamApps() == NULL) {
        return 0;
    }
    CSteamID cSteamID = SteamApps()->GetAppOwner();
    return cSteamID.ConvertToUint64();
}

// Gets the associated launch parameter if the game is run via sdk://run/<appid>/?param1=value1;param2=value2;param3=value3 etc.
SW_PY const char *GetLaunchQueryParam(const char *key) {
    if (SteamApps() == NULL) {
        return "";
    }
    return SteamApps()->GetLaunchQueryParam(key);
}

// Return the build ID for this app; will change based on backend updates.
SW_PY int GetAppBuildId() {
    if (SteamApps() == NULL) {
        return 0;
    }
    return SteamApps()->GetAppBuildId();
}

// Asynchronously retrieves metadata details about a specific file in the depot manifest.
SW_PY void GetFileDetails(const char *filename) {
    if (SteamApps() == NULL) {
        return;
    }
    SteamApps()->GetFileDetails(filename);
}

/////////////////////////////////////////////////
///// FRIENDS ///////////////////////////////////
/////////////////////////////////////////////////
//
SW_PY int GetFriendCount(int flag) {
    if (SteamFriends() == NULL) {
        return 0;
    }
    return SteamFriends()->GetFriendCount(flag);
}

SW_PY uint64 GetFriendByIndex(int thisFriend) {
    CSteamID friendID = SteamFriends()->GetFriendByIndex(thisFriend, 0xFFFF);
    return friendID.ConvertToUint64();
}

SW_PY const char *GetPersonaName() {
    if (SteamFriends() == NULL) {
        return "";
    }
    return SteamFriends()->GetPersonaName();
}

SW_PY int GetPersonaState() {
    if (SteamFriends() == NULL) {
        return 0;
    }
    return SteamFriends()->GetPersonaState();
}

SW_PY const char *GetFriendPersonaName(int steamID) {
    if (SteamFriends() != NULL && steamID > 0) {
        // Add 1 here to prevent error
        CSteamID friendID = CreateSteamID(steamID, 1);
        bool isDataLoading = SteamFriends()->RequestUserInformation(friendID, true);
        if (!isDataLoading) {
            return SteamFriends()->GetFriendPersonaName(friendID);
        }
    }
    return "";
}

SW_PY void SetGameInfo(const char *serverKey, const char *serverValue) {
    if (SteamFriends() == NULL) {
        return;
    }
    SteamFriends()->SetRichPresence(serverKey, serverValue);
}

SW_PY void ClearGameInfo() {
    if (SteamFriends() == NULL) {
        return;
    }
    SteamFriends()->ClearRichPresence();
}

SW_PY void InviteFriend(int steamID, const char *conString) {
    if (SteamFriends() == NULL) {
        return;
    }
    CSteamID friendID = CreateSteamID(steamID, 1);
    SteamFriends()->InviteUserToGame(friendID, conString);
}

SW_PY void SetPlayedWith(int steamID) {
    if (SteamFriends() == NULL) {
        return;
    }
    CSteamID friendID = CreateSteamID(steamID, 1);
    SteamFriends()->SetPlayedWith(friendID);
}

// SW_PY GetRecentPlayers
// SW_PY GetFriendAvatar
// SW_PY DrawAvatar
SW_PY void ActivateGameOverlay(const char *name) {
    if (SteamFriends() == NULL) {
        return;
    }
    return SteamFriends()->ActivateGameOverlay(name);
}

SW_PY void ActivateGameOverlayToUser(const char *url, int steamID) {
    if (SteamFriends() == NULL) {
        return;
    }
    CSteamID overlayUserID = CreateSteamID(steamID, 1);
    return SteamFriends()->ActivateGameOverlayToUser(url, overlayUserID);
}

SW_PY void ActivateGameOverlayToWebPage(const char *url) {
    if (SteamFriends() == NULL) {
        return;
    }
    return SteamFriends()->ActivateGameOverlayToWebPage(url);
}

SW_PY void ActivateGameOverlayToStore(int app_id) {
    if (SteamFriends() == NULL) {
        return;
    }
    return SteamFriends()->ActivateGameOverlayToStore(AppId_t(app_id), EOverlayToStoreFlag(0));
}

SW_PY void ActivateGameOverlayInviteDialog(int steamID) {
    if (SteamFriends() == NULL) {
        return;
    }
    CSteamID lobbyID = CreateSteamID(steamID, 1);
    return SteamFriends()->ActivateGameOverlayInviteDialog(lobbyID);
}

/////////////////////////////////////////////////
///// CONTROLLERS////////////////////////////////
/////////////////////////////////////////////////
//
// Reconfigure the controller to use the specified action set.
SW_PY void ActivateActionSet(uint64_t controllerHandle, uint64_t actionSetHandle){
    if(SteamController() == NULL){
        return;
    }
    SteamController()->ActivateActionSet((ControllerHandle_t) controllerHandle, (ControllerActionSetHandle_t)actionSetHandle);
}
// Lookup the handle for an Action Set.
SW_PY uint64_t GetActionSetHandle(const char *actionSetName) {
    if (SteamController() == NULL) {
        return 0;
    }
    return (uint64_t) SteamController()->GetActionSetHandle(actionSetName);
}

// Returns the current state of the supplied analog game action.
//SW_PY Dictionary GetAnalogActionData(uint64_t controllerHandle, uint64_t analogActionHandle){
//	ControllerAnalogActionData_t data;
//	Dictionary d;
//	memset(&data, 0, sizeof(data));
//	if(SteamController() == NULL){
//		data = SteamController()->GetAnalogActionData((ControllerHandle_t)controllerHandle, (ControllerAnalogActionHandle_t)analogActionHandle);
//	}
//	d["eMode"] = data.eMode;
//	d["x"] = data.x;
//	d["y"] = data.y;
//	d["bActive"] = data.bActive;
//	return d;
//}
// Get the handle of the specified Analog action.
SW_PY uint64_t GetAnalogActionHandle(const char *actionName) {
    if (SteamController() == NULL) {
        return 0;
    }
    return (uint64_t) SteamController()->GetAnalogActionHandle(actionName);
}

// Get the origin(s) for an analog action within an action.
//SW_PY Array GetAnalogActionOrigins(uint64_t controllerHandle, uint64_t actionSetHandle, uint64_t analogActionHandle){
//	Array list;
//	if(SteamController() == NULL){
//		EControllerActionOrigin out[STEAM_CONTROLLER_MAX_ORIGINS];
//		int ret = SteamController()->GetAnalogActionOrigins((ControllerHandle_t)controllerHandle, (ControllerActionSetHandle_t)actionSetHandle, (ControllerAnalogActionHandle_t)analogActionHandle, out);
//		for (int i = 0; i < ret; i++){
//			list.push_back((int)out[i]);
//		}
//	}
//	return list;
//}
// Get current controllers handles.
//SW_PY Array GetConnectedControllers(){
//	Array list;
//	if(SteamController() == NULL){
//		ControllerHandle_t handles[STEAM_CONTROLLER_MAX_COUNT];
//		int ret = SteamController()->GetConnectedControllers(handles);
//		for (int i = 0; i < ret; i++){
//			list.push_back((uint64_t)handles[i]);
//		}
//	}
//	return list;
//}
// Returns the associated controller handle for the specified emulated gamepad.
SW_PY uint64_t GetControllerForGamepadIndex(int index) {
    if (SteamController() == NULL) {
        return 0;
    }
    return (uint64_t) SteamController()->GetControllerForGamepadIndex(index);
}

// Get the currently active action set for the specified controller.
SW_PY uint64_t GetCurrentActionSet(uint64_t controllerHandle){
    if(SteamController() == NULL){
        return 0;
    }
    return (uint64_t) SteamController()->GetCurrentActionSet((ControllerHandle_t) controllerHandle);
}
// Get the input type (device model) for the specified controller. 
SW_PY uint64_t GetInputTypeForHandle(uint64_t controllerHandle){
    if(SteamController() == NULL){
        return 0;
    }
    return (uint64_t) SteamController()->GetInputTypeForHandle((ControllerHandle_t)controllerHandle);
}
// Returns the current state of the supplied digital game action.
//SW_PY Dictionary GetDigitalActionData(uint64_t controllerHandle, uint64_t digitalActionHandle){
//	ControllerDigitalActionData_t data;
//	Dictionary d;
//	memset(&data, 0, sizeof(data));
//	if(SteamController() == NULL){
//		data = SteamController()->GetDigitalActionData((ControllerHandle_t)controllerHandle, (ControllerDigitalActionHandle_t)digitalActionHandle);
//	}
//	d["bState"] = data.bState;
//	d["bActive"] = data.bActive;
//	return d;
//}
// Get the handle of the specified digital action.
SW_PY uint64_t GetDigitalActionHandle(const char *actionName) {
    if (SteamController() == NULL) {
        return 0;
    }
    return (uint64_t) SteamController()->GetDigitalActionHandle(actionName);
}

// Get the origin(s) for an analog action within an action.
//SW_PY Array GetDigitalActionOrigins(uint64_t controllerHandle, uint64_t actionSetHandle, uint64_t digitalActionHandle){
//	Array list;
//	if(SteamController() == NULL){
//		EControllerActionOrigin out[STEAM_CONTROLLER_MAX_ORIGINS];
//		int ret = SteamController()->GetDigitalActionOrigins((ControllerHandle_t)controllerHandle, (ControllerActionSetHandle_t)actionSetHandle, (ControllerDigitalActionHandle_t)digitalActionHandle, out);
//		for (int i=0; i<ret; i++){
//			list.push_back((int)out[i]);
//		}
//	}
//	return list;
//}
// Returns the associated gamepad index for the specified controller.
SW_PY int GetGamepadIndexForController(uint64_t controllerHandle){
    if(SteamController() == NULL){
        return -1;
    }
    return SteamController()->GetGamepadIndexForController((ControllerHandle_t) controllerHandle);
}

// Returns raw motion data for the specified controller.
//SW_PY Dictionary GetMotionData(uint64_t controllerHandle){
//	ControllerMotionData_t data;
//	Dictionary d;
//	memset(&data, 0, sizeof(data));
//	if(SteamController() == NULL){
//		data = SteamController()->GetMotionData((ControllerHandle_t)controllerHandle);
//	}
//	d["rotQuatX"] = data.rotQuatX;
//	d["rotQuatY"] = data.rotQuatY;
//	d["rotQuatZ"] = data.rotQuatZ;
//	d["rotQuatW"] = data.rotQuatW;
//	d["posAccelX"] = data.posAccelX;
//	d["posAccelY"] = data.posAccelY;
//	d["posAccelZ"] = data.posAccelZ;
//	d["rotVelX"] = data.rotVelX;
//	d["rotVelY"] = data.rotVelY;
//	d["rotVelZ"] = data.rotVelZ;
//	return d;
//}
// Start SteamControllers interface.
SW_PY bool ControllerInit() {
    if (SteamController() == NULL) {
        return false;
    }
    return SteamController()->Init();
}

// Syncronize controllers.
SW_PY void RunFrame() {
    if (SteamController() == NULL) {
        return;
    }
    SteamController()->RunFrame();
}

// Invokes the Steam overlay and brings up the binding screen.
SW_PY bool ShowBindingPanel(uint64_t controllerHandle){
    if(SteamController()== NULL){
        return false;
    }
    return SteamController()->ShowBindingPanel((ControllerHandle_t) controllerHandle);
}

// Stop SteamControllers interface.
SW_PY bool ControllerShutdown() {
    if (SteamController() == NULL) {
        return false;
    }
    return SteamController()->Shutdown();
}
// Trigger a vibration event on supported controllers.
SW_PY void TriggerVibration(uint64_t controllerHandle, uint16_t leftSpeed, uint16_t rightSpeed){
    if(SteamController()== NULL){
        return;
    }
    SteamController()->TriggerVibration((ControllerHandle_t) controllerHandle, (unsigned short)leftSpeed, (unsigned short)rightSpeed);
}

/////////////////////////////////////////////////
///// MATCHMAKING
/////////////////////////////////////////////////
//
SW_PY void CreateLobby(int lobbyType, int cMaxMembers) {
    if (SteamMatchmaking() == NULL) {
        return;
    }
    ELobbyType eLobbyType;
    // Convert the lobby type back over
    if (lobbyType == PRIVATE) {
        eLobbyType = k_ELobbyTypePrivate;
    } else if (lobbyType == FRIENDS_ONLY) {
        eLobbyType = k_ELobbyTypeFriendsOnly;
    } else if (lobbyType == PUBLIC) {
        eLobbyType = k_ELobbyTypePublic;
    } else {
        eLobbyType = k_ELobbyTypeInvisible;
    }
    SteamMatchmaking()->CreateLobby(eLobbyType, cMaxMembers);
}

SW_PY void JoinLobby(int steamIDLobby) {
    if (SteamMatchmaking() == NULL) {
        return;
    }
    CSteamID lobbyID = CreateSteamID(steamIDLobby, 1);
    SteamMatchmaking()->JoinLobby(lobbyID);
}

SW_PY void LeaveLobby(int steamIDLobby) {
    if (SteamMatchmaking() == NULL) {
        return;
    }
    CSteamID lobbyID = CreateSteamID(steamIDLobby, 1);
    return SteamMatchmaking()->LeaveLobby(lobbyID);
}

SW_PY bool InviteUserToLobby(int steamIDLobby, int steamIDInvitee) {
    if (SteamMatchmaking() == NULL) {
        return 0;
    }
    CSteamID lobbyID = CreateSteamID(steamIDLobby, 1);
    CSteamID inviteeID = CreateSteamID(steamIDInvitee, 1);
    return SteamMatchmaking()->InviteUserToLobby(lobbyID, inviteeID);
}

/////////////////////////////////////////////////
///// MUSIC /////////////////////////////////////
/////////////////////////////////////////////////
//
// Is Steam music enabled.
SW_PY bool MusicIsEnabled() {
    if (SteamMusic() == NULL) {
        return false;
    }
    return SteamMusic()->BIsEnabled();
}

// Is Steam music playing something.
SW_PY bool MusicIsPlaying() {
    if (SteamMusic() == NULL) {
        return false;
    }
    return SteamMusic()->BIsPlaying();
}

// Get the volume level of the music.
SW_PY float MusicGetVolume() {
    if (SteamMusic() == NULL) {
        return 0;
    }
    return SteamMusic()->GetVolume();
}

// Pause whatever Steam music is playing.
SW_PY void MusicPause() {
    if (SteamMusic() == NULL) {
        return;
    }
    return SteamMusic()->Pause();
}

// Play current track/album.
SW_PY void MusicPlay() {
    if (SteamMusic() == NULL) {
        return;
    }
    return SteamMusic()->Play();
}

// Play next track/album.
SW_PY void MusicPlayNext() {
    if (SteamMusic() == NULL) {
        return;
    }
    return SteamMusic()->PlayNext();
}

// Play previous track/album.
SW_PY void MusicPlayPrev() {
    if (SteamMusic() == NULL) {
        return;
    }
    return SteamMusic()->PlayPrevious();
}

// Set the volume of Steam music.
SW_PY void MusicSetVolume(float value) {
    if (SteamMusic() == NULL) {
        return;
    }
    return SteamMusic()->SetVolume(value);
}

/////////////////////////////////////////////////
///// SCREENSHOTS ///////////////////////////////
/////////////////////////////////////////////////
//
// Adds a screenshot to the user's Steam screenshot library from disk.
SW_PY uint32_t AddScreenshotToLibrary(const char *filename, const char *thumbnailFilename, int width, int height) {
    if (SteamScreenshots() == NULL) {
        return 0;
    }
    return SteamScreenshots()->AddScreenshotToLibrary(filename, thumbnailFilename, width, height);
}

// Toggles whether the overlay handles screenshots.
SW_PY void HookScreenshots(bool hook) {
    if (SteamScreenshots() == NULL) {
        return;
    }
    SteamScreenshots()->HookScreenshots(hook);
}

// Checks if the app is hooking screenshots.
SW_PY bool IsScreenshotsHooked() {
    if (SteamScreenshots() == NULL) {
        return false;
    }
    return SteamScreenshots()->IsScreenshotsHooked();
}

// Sets optional metadata about a screenshot's location.
SW_PY bool SetLocation(uint32_t screenshot, const char *location){
    if(SteamScreenshots()== NULL){
        return false;
    }
    ScreenshotHandle handle = (ScreenshotHandle) screenshot;
    return SteamScreenshots()->SetLocation(handle, location);
}

// Causes Steam overlay to take a screenshot.
SW_PY void TriggerScreenshot() {
    if (SteamScreenshots() == NULL) {
        return;
    }
    SteamScreenshots()->TriggerScreenshot();
}

/////////////////////////////////////////////////
///// USERS /////////////////////////////////////
/////////////////////////////////////////////////
//
// Get user's Steam ID.
SW_PY uint64_t GetSteamID() {
    if (SteamUser() == NULL) {
        return 0;
    }
    CSteamID steamID = SteamUser()->GetSteamID();
    return steamID.ConvertToUint64();
}

// Check, true/false, if user is logged into Steam currently.
SW_PY bool LoggedOn() {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUser()->BLoggedOn();
}

// Get the user's Steam level.
SW_PY int GetPlayerSteamLevel() {
    if (SteamUser() == NULL) {
        return 0;
    }
    return SteamUser()->GetPlayerSteamLevel();
}

// Get the user's Steam installation path (this function is depreciated).
SW_PY const char *GetUserDataFolder() {
    if (SteamUser() == NULL) {
        return "";
    }
    const int bufferSize = 256;
    char *buffer = new char[bufferSize];
    SteamUser()->GetUserDataFolder((char *) buffer, bufferSize);
    char *data_path = buffer;
    delete buffer;
    return data_path;
}

// Trading Card badges data access, if you only have one set of cards, the series will be 1.
// The user has can have two different badges for a series; the regular (max level 5) and the foil (max level 1).
SW_PY int GetGameBadgeLevel(int series, bool foil) {
    if (SteamUser() == NULL) {
        return 0;
    }
    return SteamUser()->GetGameBadgeLevel(series, foil);
}

// Returns the info needed to obtain a Session Ticket.
SW_PY int GetAuthSessionTicket(char* buffer) {
    if (SteamUser() == NULL) {
        return 0;
    }
    uint32 size{};
    SteamUser()->GetAuthSessionTicket(buffer, 1024, &size);
    return size;
}

/////////////////////////////////////////////////
///// USER STATS ////////////////////////////////
/////////////////////////////////////////////////
//
SW_PY bool ClearAchievement(const char *name) {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->ClearAchievement(name);
}

SW_PY bool GetAchievement(const char *name) {
    if (SteamUser() == NULL) {
        return "";
    }
    bool achieved = false;
    SteamUserStats()->GetAchievement(name, &achieved);
    return achieved;
}

SW_PY int GetNumAchievements(){
    if (SteamUser() == NULL){
        return 0;
    }
    return SteamUserStats()->GetNumAchievements();
}

SW_PY const char *GetAchievementName(int index){
    return SteamUserStats()->GetAchievementName(index);
}

SW_PY const char *GetAchievementDisplayAttribute(const char *name, const char *key) {
    return SteamUserStats()->GetAchievementDisplayAttribute(name, key);
}

SW_PY float GetStatFloat(const char *name) {
    if (SteamUser() == NULL) {
        return 0;
    }
    float statval = 0;
    SteamUserStats()->GetStat(name, &statval);
    return statval;
}

SW_PY int32 GetStatInt(const char *name) {
    if (SteamUser() == NULL) {
        return 0;
    }
    int32 statval = 0;
    SteamUserStats()->GetStat(name, &statval);
    return statval;
}

SW_PY bool ResetAllStats(bool achievesToo) {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->ResetAllStats(achievesToo);
}

SW_PY bool RequestCurrentStats() {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->RequestCurrentStats();
}

SW_PY bool SetAchievement(const char *name) {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->SetAchievement(name);
}

SW_PY bool SetStatFloat(const char *name, float value) {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->SetStat(name, value);
}

SW_PY bool SetStatInt(const char *name, int32 value) {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->SetStat(name, value);
}

SW_PY bool StoreStats() {
    if (SteamUser() == NULL) {
        return false;
    }
    return SteamUserStats()->StoreStats();
}
//SW_PY const char* GetLeaderboardName()
//SW_PY int GetLeaderboardEntryCount()
//SW_PY void DownloadLeaderboardEntries()
//SW_PY void DownloadLeaderboardEntriesForUsers()
//SW_PY void UploadLeaderboardScore()
//SW_PY void GetDownloadLeaderboardEntry()
//SW_PY void UpdateLeaderboardHandle()
//SW_PY uint64 GetLeaderboardHandle()
//SW_PY void GetLeaderBoardEntries()

////////////////////////////////////////////////
///// UTILS /////////////////////////////////////
/////////////////////////////////////////////////
//
// Checks if the Overlay needs a present. Only required if using event driven render updates.
SW_PY bool OverlayNeedsPresent() {
    if (SteamUtils() == NULL) {
        return false;
    }
    return SteamUtils()->BOverlayNeedsPresent();
}

// Get the Steam ID of the running application/game.
SW_PY int GetAppID() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetAppID();
}

// Get the amount of battery power, clearly for laptops.
SW_PY int GetCurrentBatteryPower() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetCurrentBatteryPower();
}

// Returns the number of IPC calls made since the last time this function was called.
SW_PY uint32 GetIPCCallCount() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetIPCCallCount();
}

// Get the user's country by IP.
SW_PY const char *GetIPCountry() {
    if (SteamUtils() == NULL) {
        return "None";
    }
    return SteamUtils()->GetIPCountry();
}

SW_PY uint32 GetSecondsSinceAppActive() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetSecondsSinceAppActive();
}

SW_PY uint32 GetSecondsSinceComputerActive() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetSecondsSinceComputerActive();
}

SW_PY uint32 GetServerRealTime() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->GetServerRealTime();
}

// Get the Steam user interface language.
SW_PY const char *GetSteamUILanguage() {
    if (SteamUtils() == NULL) {
        return "None";
    }
    return SteamUtils()->GetSteamUILanguage();
}

// Returns true/false if Steam overlay is enabled.
SW_PY bool IsOverlayEnabled() {
    if (SteamUtils() == NULL) {
        return false;
    }
    return SteamUtils()->IsOverlayEnabled();
}

// Returns true if Steam & the Steam Overlay are running in Big Picture mode.
SW_PY bool IsSteamInBigPictureMode() {
    if (SteamUtils() == NULL) {
        return false;
    }
    return SteamUtils()->IsSteamInBigPictureMode();
}

// Is Steam running in VR?
SW_PY bool IsSteamRunningInVR() {
    if (SteamUtils() == NULL) {
        return 0;
    }
    return SteamUtils()->IsSteamRunningInVR();
}

// Checks if the HMD view will be streamed via Steam In-Home Streaming.
SW_PY bool IsVRHeadsetStreamingEnabled() {
    if (SteamUtils() == NULL) {
        return false;
    }
    return SteamUtils()->IsVRHeadsetStreamingEnabled();
}

// Sets the inset of the overlay notification from the corner specified by SetOverlayNotificationPosition.
SW_PY void SetOverlayNotificationInset(int horizontal, int vertical) {
    if (SteamUtils() == NULL) {
        return;
    }
    SteamUtils()->SetOverlayNotificationInset(horizontal, vertical);
}

// Set the position where overlay shows notifications.
SW_PY void SetOverlayNotificationPosition(int pos) {
    if ((pos < 0) || (pos > 3) || (SteamUtils() == NULL)) {
        return;
    }
    SteamUtils()->SetOverlayNotificationPosition(ENotificationPosition(pos));
}

// Set whether the HMD content will be streamed via Steam In-Home Streaming.
SW_PY void SetVRHeadsetStreamingEnabled(bool enabled) {
    if (SteamUtils() == NULL) {
        return;
    }
    SteamUtils()->SetVRHeadsetStreamingEnabled(enabled);
}

// Activates the Big Picture text input dialog which only supports gamepad input.
SW_PY bool ShowGamepadTextInput(int inputMode, int lineInputMode, const char *description, uint32 maxText,
                                const char *presetText) {
    if (SteamUtils() == NULL) {
        return false;
    }
    // Convert modes
    EGamepadTextInputMode mode;
    if (inputMode == 0) {
        mode = k_EGamepadTextInputModeNormal;
    } else {
        mode = k_EGamepadTextInputModePassword;
    }
    EGamepadTextInputLineMode lineMode;
    if (lineInputMode == 0) {
        lineMode = k_EGamepadTextInputLineModeSingleLine;
    } else {
        lineMode = k_EGamepadTextInputLineModeMultipleLines;
    }
    return SteamUtils()->ShowGamepadTextInput(mode, lineMode, description, maxText, presetText);
}

// Ask SteamUI to create and render its OpenVR dashboard.
SW_PY void StartVRDashboard() {
    if (SteamUtils() == NULL) {
        return;
    }
    SteamUtils()->StartVRDashboard();
}

//-----------------------------------------------
// Steam Workshop
//-----------------------------------------------
SW_PY void Workshop_SetItemCreatedCallback(CreateItemResultCallback_t callback) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.SetItemCreatedCallback(callback);
}

SW_PY void Workshop_CreateItem(AppId_t consumerAppId, EWorkshopFileType fileType) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.CreateItem(consumerAppId, fileType);
}

SW_PY UGCUpdateHandle_t Workshop_StartItemUpdate(AppId_t consumerAppId, PublishedFileId_t publishedFileId){
    return SteamUGC()->StartItemUpdate(consumerAppId, publishedFileId);
}

SW_PY bool Workshop_SetItemTitle(UGCUpdateHandle_t updateHandle, const char *pTitle){
    if(SteamUGC() == NULL){
        return false;
    }
    if (strlen(pTitle) > UGC_MAX_TITLE_CHARS){
        printf("Title cannot have more than %d ASCII characters. Title not set.", UGC_MAX_TITLE_CHARS);
        return false;
    }
    return SteamUGC()->SetItemTitle(updateHandle, pTitle);
}

SW_PY bool Workshop_SetItemDescription(UGCUpdateHandle_t updateHandle, const char *pDescription){
    if(SteamUGC() == NULL){
        return false;
    }
    if (strlen(pDescription) > UGC_MAX_DESC_CHARS){
        printf("Description cannot have more than %d ASCII characters. Description not set.", UGC_MAX_DESC_CHARS);
        return false;
    }
    return SteamUGC()->SetItemDescription(updateHandle, pDescription);
}

SW_PY bool Workshop_SetItemUpdateLanguage(UGCUpdateHandle_t updateHandle, const char *pLanguage){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->SetItemUpdateLanguage(updateHandle, pLanguage);
}

SW_PY bool Workshop_SetItemMetadata(UGCUpdateHandle_t updateHandle, const char *pMetadata){
    if(SteamUGC() == NULL){
        return false;
    }
    if (strlen(pMetadata) > UGC_MAX_METADATA_CHARS){
        printf("Metadata cannot have more than %d ASCII characters. Metadata not set.", UGC_MAX_METADATA_CHARS);
    }
    return SteamUGC()->SetItemMetadata(updateHandle, pMetadata);
}

SW_PY bool Workshop_SetItemVisibility(UGCUpdateHandle_t updateHandle, ERemoteStoragePublishedFileVisibility visibility){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->SetItemVisibility(updateHandle, visibility);
}

SW_PY bool Workshop_SetItemTags(UGCUpdateHandle_t updateHandle, const char **stringArray, const int32 stringCount){
    if(SteamUGC() == NULL){
        return false;
    }
    SteamParamStringArray_t tags = {stringArray, stringCount};
    return SteamUGC()->SetItemTags(updateHandle, &tags);
}

SW_PY bool Workshop_SetItemContent(UGCUpdateHandle_t updateHandle, const char *pContentFolder){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->SetItemContent(updateHandle, pContentFolder);
}

SW_PY bool Workshop_SetItemPreview(UGCUpdateHandle_t updateHandle, const char *pPreviewFile){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->SetItemPreview(updateHandle, pPreviewFile);
}

SW_PY void Workshop_SetItemUpdatedCallback(SubmitItemUpdateResultCallback_t callback) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.SetItemUpdatedCallback(callback);
}

SW_PY void Workshop_SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *pChangeNote){
    if(SteamUGC() == NULL){
        return;
    }
    workshop.SubmitItemUpdate(updateHandle, pChangeNote);
}

SW_PY void Workshop_SubscribeItem(PublishedFileId_t publishedFileID){
    if(SteamUGC() == NULL){
        return;
    }
    workshop.SubscribeItem(publishedFileID);
}

SW_PY void Workshop_UnsubscribeItem(PublishedFileId_t publishedFileID){
    if(SteamUGC() == NULL){
        return;
    }
    workshop.UnsubscribeItem(publishedFileID);
}

SW_PY EItemUpdateStatus Workshop_GetItemUpdateProgress(UGCUpdateHandle_t handle, uint64 *punBytesProcessed, uint64 * punBytesTotal){
    return SteamUGC()->GetItemUpdateProgress(handle, punBytesProcessed, punBytesTotal);
}

SW_PY uint32 Workshop_GetNumSubscribedItems() {
    if (SteamUGC() == NULL) {
        return 0;
    }
    return SteamUGC()->GetNumSubscribedItems();
}

SW_PY uint32 Workshop_GetSubscribedItems(PublishedFileId_t * pvecPublishedFileID, uint32 maxEntries){
    if(SteamUGC() == NULL){
        return 0;
    }
    return SteamUGC()->GetSubscribedItems(pvecPublishedFileID, maxEntries);
}

SW_PY uint32 Workshop_GetItemState(PublishedFileId_t publishedFileID){
    if(SteamUGC() == NULL){
        return 0;
    }
    return SteamUGC()->GetItemState(publishedFileID);
}

SW_PY void Workshop_SetItemInstalledCallback(ItemInstalledCallback_t callback) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.SetItemInstalledCallback(callback);
}

SW_PY void Workshop_ClearItemInstalledCallback() {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.ClearItemInstallCallback();
}

SW_PY void Workshop_SetItemSubscribedCallback(RemoteStorageSubscribeFileResultCallback_t callback) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.SetItemSubscribedCallback(callback);
}

SW_PY void Workshop_SetItemUnsubscribedCallback(RemoteStorageUnsubscribeFileResultCallback_t callback) {
    if (SteamUGC() == NULL) {
        return;
    }
    workshop.SetItemUnsubscribedCallback(callback);
}

SW_PY bool Workshop_GetItemInstallInfo(PublishedFileId_t nPublishedFileID, uint64 *punSizeOnDisk, char *pchFolder, uint32 cchFolderSize, uint32 *punTimeStamp){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->GetItemInstallInfo(nPublishedFileID, punSizeOnDisk, pchFolder, cchFolderSize, punTimeStamp);
}

SW_PY bool Workshop_GetItemDownloadInfo(PublishedFileId_t publishedFileID, uint64 *punBytesDownloaded, uint64 *punBytesTotal){
    if(SteamUGC() == NULL){
        return false;
    }
    return SteamUGC()->GetItemDownloadInfo(publishedFileID, punBytesDownloaded, punBytesTotal);
}

SW_PY void Workshop_SuspendDownloads(bool bSuspend) {
    if (SteamUGC() == NULL) {
        return;
    }
    SteamUGC()->SuspendDownloads(bSuspend);
}

//-----------------------------------------------
// Steam Leaderboard
//-----------------------------------------------
SW_PY void Leaderboard_SetFindLeaderboardResultCallback(LeaderboardFindResultCallback_t callback) {
    if (SteamUserStats() == NULL) {
        return;
    }
    leaderboard.SetLeaderboardFindResultCallback(callback);
}

SW_PY void Leaderboard_FindLeaderboard(const char *pchLeaderboardName) {
    if (SteamUserStats() == NULL) {
        return;
    }
    leaderboard.FindLeaderboard(pchLeaderboardName);
}

//-----------------------------------------------
// Steam MicroTxn
//-----------------------------------------------
SW_PY void MicroTxn_SetAuthorizationResponseCallback(MicroTxnAuthorizationResponseCallback_t callback) {
    if (SteamUser() == NULL) {
        return;
    }
    microtxn.SetAuthorizationResponseCallback(callback);
}