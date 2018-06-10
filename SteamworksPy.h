/////////////////////////////////////////////////
///// STEAMWORKS FOR PYTHON HEADER
/////////////////////////////////////////////////
//
// Modify SW_PY based on operating system and include the proper Steamworks API file
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
// Include C++ headers
#include <vector>

using std::vector;

// Start the Steam class
class Steam {
	public:
		enum {
			OFFLINE=0, ONLINE=1, BUSY=2, AWAY=3, SNOOZE=4, LF_TRADE, LF_PLAY, STATE_MAX, NOT_OFFLINE=8, ALL=9,
			TOP_LEFT=0, TOP_RIGHT=1, BOT_LEFT=2, BOT_RIGHT=3,
			OK=0, FAILED=1, ERR_NO_CLIENT=2, ERR_NO_CONNECTION=3,
			AUTH_SESSION_OK=0, AUTH_SESSION_STEAM_NOT_CONNECTED=1, AUTH_SESSION_NO_LICENSE=2, AUTH_SESSION_VAC_BANNED=3, AUTH_SESSION_LOGGED_IN_ELSEWHERE=4,
			AUTH_SESSION_VAC_CHECK_TIMEOUT=5, AUTH_SESSION_TICKET_CANCELED=6, AUTH_SESSION_TICKET_ALREADY_USED=7, AUTH_SESSION_TICKET_INVALID=8, AUTH_SESSION_PUBLISHER_BANNED=9,
			AVATAR_SMALL=0, AVATAR_MEDIUM, AVATAR_LARGE,
			GLOBAL=0, GLOBAL_AROUND_USER=1, FRIENDS=2, USERS=3,
			LOBBY_OK=0, LOBBY_NO_CONNECTION=1, LOBBY_TIMEOUT=2, LOBBY_FAIL=3, LOBBY_ACCESS_DENIED=4, LOBBY_LIMIT_EXCEEDED=5,
			PRIVATE=0, FRIENDS_ONLY=1, PUBLIC=2, INVISIBLE=3, LOBBY_KEY_LENGTH=255,
			REMOTE_STORAGE_PLATFORM_NONE=0, REMOTE_STORAGE_PLATFORM_WINDOWS=(1<<0), REMOTE_STORAGE_PLATFORM_OSX=(1<<1), REMOTE_STORAGE_PLATFORM_PS3=(1<<2), 
			REMOTE_STORAGE_PLATFORM_LINUX=(1<<3), REMOTE_STORAGE_PLATFORM_RESERVED2=(1<<4), REMOTE_STORAGE_PLATFORM_ALL=0xffffffff,
			UGC_MAX_TITLE_CHARS=128, UGC_MAX_DESC_CHARS=8000, UGC_MAX_METADATA_CHARS=5000,
			UGC_ITEM_COMMUNITY=0, UGC_ITEM_MICROTRANSACTION=1, UGC_ITEM_COLLECTION=2, UGC_ITEM_ART=3, UGC_ITEM_VIDEO=4, UGC_ITEM_SCREENSHOT=5, UGC_ITEM_GAME=6, UGC_ITEM_SOFTWARE=7,
			UGC_ITEM_CONCEPT=8, UGC_ITEM_WEBGUIDE=9, UGC_ITEM_INTEGRATEDGUIDE=10, UGC_ITEM_MERCH=11, UGC_ITEM_CONTROLLERBINDING=12, UGC_ITEM_STEAMWORKSACCESSINVITE=13,
			UGC_ITEM_STEAMVIDEO=14, UGC_ITEM_GAMEMANAGEDITEM=15, UGC_ITEM_MAX=16,
			UGC_STATE_NONE=0, UGC_STATE_SUBSCRIBED=1, UGC_STATE_LEGACY=2, UGC_STATE_INSTALLED=4, UGC_STATE_UPDATE=8, UGC_STATE_DOWNLOADING=16, UGC_STATE_PENDING=32,
			STATUS_INVALID=0, STATUS_PREPARING_CONFIG=1, STATUS_PREPARING_CONTENT=2, STATUS_UPLOADING_CONTENT=3, STATUS_UPLOADING_PREVIEW=4, STATUS_COMMITTING_CHANGES=5
		};
		Steam();
		~Steam();

		CSteamID CreateSteamID(uint32 steamID, int accountType=-1);
//		Image DrawAvatar(int image);
		// Steamworks ///////////////////////////////
		bool RestartAppIfNecessary(int value);
		bool SteamInit();
		bool IsSteamRunning();
		// Apps /////////////////////////////////////
		bool HasOtherApp(int value);
		int GetDLCCount();
		bool IsDLCInstalled(int value);
		bool IsAppInstalled(int value);
		const char* GetCurrentGameLanguage();
		bool IsVACBanned();
		int GetEarliestPurchaseUnixTime(int value);
		bool IsSubscribedFromFreeWeekend();
		void InstallDLC(int value);
		void UninstallDLC(int value);
		bool IsSubscribed();
		bool IsLowViolence();
		bool IsCybercafe();
		bool IsSubscribedApp(int value);
		int GetAppBuildId();
		// Controller ///////////////////////////////
		void ActivateActionSet(ControllerHandle_t controllerHandle, ControllerActionSetHandle_t actionSetHandle);
		ControllerActionSetHandle_t GetActionSetHandle(const char *actionSetName);
		ControllerAnalogActionData_t GetAnalogActionData(ControllerHandle_t controllerHandle, ControllerAnalogActionHandle_t analogActionHandle);
		ControllerAnalogActionHandle_t GetAnalogActionHandle(const char *actionName);
		int GetAnalogActionOrigins(ControllerHandle_t controllerHandle, ControllerActionSetHandle_t actionSetHandle, ControllerAnalogActionHandle_t analogActionHandle, EControllerActionOrigin *originsOut);
		int GetConnectedControllers(ControllerHandle_t *handlesOut);
		ControllerHandle_t GetControllerForGamepadIndex(int index);
		ControllerActionSetHandle_t GetCurrentActionSet(ControllerHandle_t controllerHandle);
		ControllerDigitalActionData_t GetDigitalActionData(ControllerHandle_t controllerHandle, ControllerDigitalActionHandle_t digitalActionHandle);
		ControllerDigitalActionHandle_t GetDigitalActionHandle(const char *actionName);
		int GetDigitalActionOrigins(ControllerHandle_t controllerHandle, ControllerActionSetHandle_t actionSetHandle, ControllerDigitalActionHandle_t digitalActionHandle, EControllerActionOrigin *originsOut);
		int GetGamepadIndexForController(ControllerHandle_t controllerHandle);
		ControllerMotionData_t GetMotionData(ControllerHandle_t controllerHandle);
		bool ControllerInit();
		void RunFrame();
		bool showBindingPanel(ControllerHandle_t controllerHandle);
		bool ControllerShutdown();
		void TriggerVibration(ControllerHandle_t controllerHandle, uint16 leftSpeed, uint16 rightSpeed);
		// Friends //////////////////////////////////
		int GetFriendCount();
		const char* GetPersonaName();
		const char* GetFriendPersonaName(int steamID);
		void SetGameInfo(const char* key, const char* value);
		void ClearGameInfo();
		void InviteFriend(int id, const char* connectString);
		void SetPlayedWith(int steamID);
		void GetFriendAvatar(int size=AVATAR_MEDIUM);
		const char* GetUserSteamFriends();
		void ActivateGameOverlay(const char* type);
		void ActivateGameOverlayToUser(const char* type, int steamID);
		void ActivateGameOverlayToWebPage(const char* url);
		void ActivateGameOverlayToStore(int appid=0);
		void ActivateGameOverlayInviteDialog(int steamID);
		// Matchmaking //////////////////////////////
		void CreateLobby(int lobbyType, int maxMembers);
		void JoinLobby(int steamIDLobby);
		void LeaveLobby(int steamIDLobby);
		bool InviteUserToLobby(int steamIDLobby, int steamIDInvitee);
		// Music ////////////////////////////////////
		bool MusicIsEnabled();
		bool MusicIsPlaying();
		float MusicGetVolume();
		void MusicPause();
		void MusicPlay();
		void MusicPlayNext();
		void MusicPlayPrev();
		void MusicSetVolume(float value);
		// Remote Storage ///////////////////////////
//		bool FileWrite(const char* file, const void *data, int32 dataSize);
//		int32 FileRead(const char* file, void *data, int32 dataToRead);
		bool FileForget(const char* file);
		bool FileDelete(const char* file);
		bool FileExists(const char* file);
		bool FilePersisted(const char* file);
		int32 GetFileSize(const char* file);
		int64 GetFileTimestamp(const char* file);
		int32 GetFileCount();
		bool IsCloudEnabledForAccount();
		bool IsCloudEnabledForApp();
		void SetCloudEnabledForApp(bool enabled);
//		const char *GetFileNameAndSize(int file);
//		bool GetQuota();
		uint32 GetSyncPlatforms(const char* file);
		// Screenshots //////////////////////////////
		ScreenshotHandle AddScreenshotToLibrary(const char *filename, const char *thumbnailFilename, int width, int height);
		void HookScreenshots(bool hook);
		bool IsScreenshotsHooked();
		bool SetLocation(uint32 screenshot, const char *location);
		void TriggerScreenshot();
//		ScreenshotHandle WriteScreenshot(void *RGB, uint32 dataRGB, int width, int height);
		// Users ////////////////////////////////////
//		uint32 GetAuthSessionTicket();
//		void CancelAuthTicket(uint32 authTicket);
//		int BeginAuthSession(uint32 authTicket, uint64 steamID);
		void EndAuthSession(uint64 steamID);
		uint64 GetSteamID();
		bool LoggedOn();
		int GetPlayerSteamLevel();
//		bool GetUserDataFolder(char* buffer, int bufferSize=0);
//		void AdvertiseGame(CSteamID steamIDGameServer, uint32 serverIP, uint16 port);
		int GetGameBadgeLevel(int series, bool foil);
		// User Stats ///////////////////////////////
		bool ClearAchievement(const char *name);
		uint32 GetNumAchievements();
		void GetNumberOfCurrentPlayers();
		bool GetAchievement(const char *name);
//		bool GetAchievementAchievedPercent(const char* name, float *percent=0);
		float GetStatFloat(const char* name);
		int GetStatInt(const char* name);
		bool ResetAllStats(bool achievementsToo=0);
		bool RequestCurrentStats();
//		SteamAPICall_t RequestGlobalAchievementPercentages();
		bool SetAchievement(const char* name);
		bool SetStatFloat(const char* name, float value=0);
		bool SetStatInt(const char* name, int value=0);
		bool StoreStats();
//		SteamAPICall_t FindLeaderboard(const char* name);
//		const char *GetLeaderboardName();
//		int GetLeaderboardEntryCount(SteamLeaderboard_t hSteamLeaderboard);
//		SteamAPICall_t DownloadLeaderboardEntries(SteamLeaderboard_t hSteamLeaderboard, ELeaderboardDataRequest eLeaderboardDataRequest, int start, int end, int type=GLOBAL);
//		SteamAPICall_t DownloadLeaderboardEntriesForUsers(int usersID[]);
//		SteamAPICall_t UploadLeaderboardScore(int score, bool keepBest=0);
//		bool GetDownloadedLeaderboardEntry(SteamLeaderboardEntries_t handle, int entryCount);
		uint64 GetLeaderboardHandle();
		const char* GetLeaderboardEntries();
		bool GetAchievementAndUnlockTime(const char *name, bool *achieved, uint32 *unlockTime);
		bool IndicateAchievementProgress(const char *name, uint32 currentProgress, uint32 maxProgress);
		// Utils ////////////////////////////////////
		const char *GetIPCountry();
		bool IsOverlayEnabled();
		const char *GetSteamUILanguage();
		int GetAppID();
		int GetSecondsSinceAppActive();
		void SetOverlayNotificationPosition(int pos);
		int GetCurrentBatteryPower();
		bool IsSteamRunningInVR();
		int GetServerRealTime();
		bool IsSteamInBigPictureMode();
		void StartVRDashboard();
		// Workshop /////////////////////////////////
		bool DownloadItem(int publishedFileID, bool highPriority);
		void SuspendDownloads(bool suspend);
		uint64 StartItemUpdate(AppId_t appID, int fileId);
		int GetItemState(int publishedFileID);
		int GetItemUpdateProgress(uint64 handle, uint64 *bytesProcessed, uint64* bytesTotal);
		void CreateItem(AppId_t appID, EWorkshopFileType fileType);
		bool SetItemTitle(UGCUpdateHandle_t updateHandle, const char *title);
		bool SetItemDescription(UGCUpdateHandle_t updateHandle, const char *description);
		bool SetItemUpdateLanguage(UGCUpdateHandle_t updateHandle, const char *language);
		bool SetItemMetadata(UGCUpdateHandle_t updateHandle, const char *metadata);
		bool SetItemVisibility(UGCUpdateHandle_t updateHandle, ERemoteStoragePublishedFileVisibility visibility);
		bool SetItemTags(UGCUpdateHandle_t updateHandle, const SteamParamStringArray_t *tags);
		bool SetItemContent(UGCUpdateHandle_t updateHandle, const char *contentFolder);
		bool SetItemPreview(UGCUpdateHandle_t updateHandle, const char *previewFile);
		void SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *changeNote);
		uint32 GetSubscribedItems(PublishedFileId_t* publishedFileID, uint32 maxEntries);
		bool GetItemInstallInfo(int fileID, uint64 *sizeOnDisk, char *folder, uint32 folderSize, uint32 *timeStamp);
		bool GetItemDownloadInfo(int fileID, uint64 *bytesDownloaded, uint64 *bytesTotal);

	protected:
		static void _bind_methods();

	private:
		bool isInitSuccess;
		// Leaderboards
		SteamLeaderboard_t leaderboard_handle;
		const char* leaderboard_entries;
		// Authentication
		struct TicketData{
			uint32 id;
			uint32 *buffer;
			uint32 size;
		};
		vector<TicketData> tickets;
		// Steam Callbacks //////////////////////////
		// Callback for lobby created
		CCallResult<Steam,LobbyCreated_t> callLobbyCreated;
		void _lobby_created(LobbyCreated_t *callData);
		// Callback for lobby enter
		CCallResult<Steam, LobbyEnter_t> callLobbyEnter;
		void _lobby_joined(LobbyEnter_t *callData);
		// Callback for lobby invite
		CCallResult<Steam, LobbyInvite_t> callLobbyInvite;
		void _lobby_invite(LobbyInvite_t *callData);
		// Callback for join request
		CCallResult<Steam, GameRichPresenceJoinRequested_t> callJoinRequested;
		void _join_requested(GameRichPresenceJoinRequested_t *callData);
		// Callback for overlay activated
		CCallResult<Steam, GameOverlayActivated_t> callOverlayActivated;
		void _overlay_toggled(GameOverlayActivated_t *callData);
		// Callback for low battery power
		CCallResult<Steam, LowBatteryPower_t> callLowBattery;
		void _low_power(LowBatteryPower_t *callData);
		// Callback for avatar loading
		CCallResult<Steam, AvatarImageLoaded_t> callAvatarLoaded;
		void _avatar_loaded(AvatarImageLoaded_t *callData);
		// Callback for Steam server connecting
		CCallResult<Steam, SteamServersConnected_t> callServerConnect;
		void _server_connected(SteamServersConnected_t *callData);
		// Callback for Steam server disconnecting
		CCallResult<Steam, SteamServersDisconnected_t> callServerDisconnect;
		void _server_disconnected(SteamServersDisconnected_t *callData);
		// Callback for DLC installing
		CCallResult<Steam, DlcInstalled_t> callDLCInstall;
		void _dlc_installed(DlcInstalled_t *callData);
		// Callback for autentication response
		CCallResult<Steam, GetAuthSessionTicketResponse_t> callAuthSessionResponse;
		void _get_auth_session_ticket_response(GetAuthSessionTicketResponse_t *callData);
		// Callback for authentication ticket validating
		CCallResult<Steam, ValidateAuthTicketResponse_t> callAuthTicketValidate;
		void _validate_auth_ticket_response(ValidateAuthTicketResponse_t *callData);
		// Callback for screenshot being ready
		CCallResult<Steam, ScreenshotReady_t> callScreenshotReady;
		void _screenshot_ready(ScreenshotReady_t *callData);
		// Callback for receiving user stats
		CCallResult<Steam, UserStatsReceived_t> callReceiveUserStats;
		void _user_stats_received(UserStatsReceived_t *callData);
		// Callback for workshop item installing
		CCallResult<Steam, ItemInstalled_t> callInstallItem;
		void _workshop_item_installed(ItemInstalled_t *callData);
		// Callback for number of current players.
		CCallResult<Steam, NumberOfCurrentPlayers_t> callResultNumberOfCurrentPlayers;
		void _number_of_current_players(NumberOfCurrentPlayers_t *callData, bool bIOFailure);
		// Callback for leaderboard score uploading.
		CCallResult<Steam, LeaderboardScoreUploaded_t> callResultUploadScore;
		void _leaderboard_uploaded(LeaderboardScoreUploaded_t *callData, bool bIOFailure);
		// Callback for finding leaderboard results.
		CCallResult<Steam, LeaderboardFindResult_t> callResultFindLeaderboard;
		void _leaderboard_loaded(LeaderboardFindResult_t *callData, bool bIOFailure);
		// Callback for downloading leaderboard scores.
		CCallResult<Steam, LeaderboardScoresDownloaded_t> callResultEntries;
		void _leaderboard_entries_loaded(LeaderboardScoresDownloaded_t *callData, bool bIOFailure);
		// Callback for global achievement percentages.
		CCallResult<Steam, GlobalAchievementPercentagesReady_t> callResultGlobalAchievementPercentagesReady;
		void _global_achievement_percentages_ready(GlobalAchievementPercentagesReady_t *callData, bool bIOFailure);
		// Callback for workshop item creation
		CCallResult<Steam, CreateItemResult_t> callResultItemCreate;
		void _workshop_item_created(CreateItemResult_t *callData, bool bIOFailure);
		// Callback for workshop item updating
		CCallResult<Steam, SubmitItemUpdateResult_t> callResultItemUpdate;
		void _workshop_item_updated(SubmitItemUpdateResult_t *callData, bool bIOFailure);
		// Run the Steamworks API callbacks
		void RunCallbacks(){
			SteamAPI_RunCallbacks();
		}
};