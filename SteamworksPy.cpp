//===============================================
//  STEAMWORKS FOR PYTHON
//===============================================

// Modify SW_PY based on operating system and include the proper Steamworks API file
//-----------------------------------------------
#if defined( _WIN32 )
	#include "steam\steam_api.h"
	#define SW_PY extern "C" __declspec( dllexport )
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

#define UGC_MAX_TITLE_CHARS 128
#define UGC_MAX_DESC_CHARS 8000
#define UGC_MAX_METADATA_CHARS 5000

// Steamworks functions
//-----------------------------------------------
SW_PY bool SteamInit(void){
	return SteamAPI_Init();
}
SW_PY bool IsSteamRunning(void){
	return SteamAPI_IsSteamRunning();
}
// Steam Apps
SW_PY int GetDlcCount(){
	return SteamApps()->GetDLCCount();
}
SW_PY bool IsDlcInstalled(int32 value){
	return SteamApps()->BIsDlcInstalled(value);
}
SW_PY void RequestAppProofOfPurchaseKey(int32 value){
	return SteamApps()->RequestAppProofOfPurchaseKey(value);
}
// Steam Friends
SW_PY int GetFriendCount(int flag){
	return SteamFriends()->GetFriendCount(flag);
}
SW_PY const char* GetPersonaName(){
	return SteamFriends()->GetPersonaName();
}
SW_PY int GetPersonaState(){
	return SteamFriends()->GetPersonaState();
}
SW_PY void ActivateGameOverlay(const char* name){
	return SteamFriends()->ActivateGameOverlay(name);	
}
SW_PY void ActivateGameOverlayToWebPage(const char* url) {
	return SteamFriends()->ActivateGameOverlayToWebPage(url);
}
// Steam Music
SW_PY bool MusicIsEnabled(){
	return SteamMusic()->BIsEnabled();
}
SW_PY bool MusicIsPlaying(){
	return SteamMusic()->BIsPlaying();
}
SW_PY float MusicGetVolume(){
	return SteamMusic()->GetVolume();
}
SW_PY void MusicPause(){
	return SteamMusic()->Pause();
}
SW_PY void MusicPlay(){
	return SteamMusic()->Play();
}
SW_PY void MusicPlayNext(){
	return SteamMusic()->PlayNext();
}
SW_PY void MusicPlayPrev(){
	return SteamMusic()->PlayPrevious();
}
SW_PY void MusicSetVolume(float value){
	return SteamMusic()->SetVolume(value);
}
// Steam User
SW_PY CSteamID GetSteamID(){
	return SteamUser()->GetSteamID();
}
SW_PY int GetPlayerSteamLevel(){
	return SteamUser()->GetPlayerSteamLevel(); 
}
// Steam User Stats
SW_PY bool ClearAchievement(const char* name){
	return SteamUserStats()->ClearAchievement(name);
}
SW_PY bool GetAchievement(const char* name){
	bool achieved = false;
	SteamUserStats()->GetAchievement(name, &achieved);
	return achieved;
}
SW_PY float GetStatFloat(const char* name){
	float statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
SW_PY int32 GetStatInt(const char* name){
	int32 statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
SW_PY bool ResetAllStats(bool achievesToo){
	return SteamUserStats()->ResetAllStats(achievesToo);
}
SW_PY bool RequestCurrentStats(){
	return SteamUserStats()->RequestCurrentStats();
}
SW_PY bool SetAchievement(const char* name){
	return SteamUserStats()->SetAchievement(name);
}
SW_PY bool SetStatFloat(const char* name, float value){
	return SteamUserStats()->SetStat(name, value);
}
SW_PY bool SetStatInt(const char* name, int32 value){
	return SteamUserStats()->SetStat(name, value);
}
SW_PY bool StoreStats(){
	return SteamUserStats()->StoreStats();
}
// Steam Utilities
SW_PY uint8 GetCurrentBatteryPower(){
	return SteamUtils()->GetCurrentBatteryPower();
}
SW_PY const char* GetIPCountry(){
	return SteamUtils()->GetIPCountry();
}
SW_PY uint32 GetSecondsSinceAppActive(){
	return SteamUtils()->GetSecondsSinceAppActive();
}
SW_PY uint32 GetSecondsSinceComputerActive(){
	return SteamUtils()->GetSecondsSinceComputerActive();
}
SW_PY uint32 GetServerRealTime(){
	return SteamUtils()->GetServerRealTime();
}
SW_PY bool IsOverlayEnabled(){
	return SteamUtils()->IsOverlayEnabled();
}
SW_PY bool IsSteamRunningInVR(){
	return SteamUtils()->IsSteamRunningInVR();
}
SW_PY const char* GetSteamUILanguage(){
	return SteamUtils()->GetSteamUILanguage();
}
SW_PY uint32 GetAppID(){
	return SteamUtils()->GetAppID();
}

// Callbacks
SW_PY void RunCallbacks()
{
	SteamAPI_RunCallbacks();
}

// Workshop
typedef void(*CreateItemResultCallback_t) (CreateItemResult_t);
typedef void(*SubmitItemUpdateResultCallback_t) (SubmitItemUpdateResult_t);

class Workshop
{
public:
	CreateItemResultCallback_t _pyItemCreatedCallback;
	SubmitItemUpdateResultCallback_t _pyItemUpdatedCallback;

	CCallResult<Workshop, CreateItemResult_t> _itemCreatedCallback;
	CCallResult<Workshop, SubmitItemUpdateResult_t> _itemUpdatedCallback;

	void SetItemCreatedCallback(CreateItemResultCallback_t callback)
	{
		_pyItemCreatedCallback = callback;
	}

	void SetItemUpdatedCallback(SubmitItemUpdateResultCallback_t callback)
	{
		_pyItemUpdatedCallback = callback;
	}
	
	void CreateItem(AppId_t consumerAppId, EWorkshopFileType fileType)
	{
		//TODO: Check if fileType is a valid value?

		SteamAPICall_t createItemCall = SteamUGC()->CreateItem(consumerAppId, fileType);
		_itemCreatedCallback.Set(createItemCall, this, &Workshop::OnWorkshopItemCreated);
	}

	void SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *pChangeNote)
	{
		SteamAPICall_t submitItemUpdateCall = SteamUGC()->SubmitItemUpdate(updateHandle, pChangeNote);
		_itemUpdatedCallback.Set(submitItemUpdateCall, this, &Workshop::OnItemUpdateSubmitted);
	}

private:
	void OnWorkshopItemCreated(CreateItemResult_t* createItemResult, bool bIOFailure)
	{
		if (_pyItemCreatedCallback != nullptr) 
		{
			_pyItemCreatedCallback(*createItemResult);
		}
	}

	void OnItemUpdateSubmitted(SubmitItemUpdateResult_t* submitItemUpdateResult, bool bIOFailure)
	{
		if (_pyItemUpdatedCallback != nullptr)
		{
			_pyItemUpdatedCallback(*submitItemUpdateResult);
		}
	}
};

static Workshop workshop;

SW_PY void Workshop_SetItemCreatedCallback(CreateItemResultCallback_t callback)
{
	workshop.SetItemCreatedCallback(callback);
}

SW_PY void Workshop_CreateItem(AppId_t consumerAppId, EWorkshopFileType fileType)
{
	workshop.CreateItem(consumerAppId, fileType);
}

SW_PY UGCUpdateHandle_t Workshop_StartItemUpdate(AppId_t consumerAppId, PublishedFileId_t publishedFileId)
{
	return SteamUGC()->StartItemUpdate(consumerAppId, publishedFileId);
}

SW_PY bool Workshop_SetItemTitle(UGCUpdateHandle_t updateHandle, const char *pTitle)
{
	if (strlen(pTitle) > UGC_MAX_TITLE_CHARS)
	{
		printf("Title cannot have more than %d ASCII characters. Title not set.", UGC_MAX_TITLE_CHARS);
		return false;
	}

	return SteamUGC()->SetItemTitle(updateHandle, pTitle);
}

SW_PY bool Workshop_SetItemDescription(UGCUpdateHandle_t updateHandle, const char *pDescription)
{
	if (strlen(pDescription) > UGC_MAX_DESC_CHARS)
	{
		printf("Description cannot have more than %d ASCII characters. Description not set.", UGC_MAX_DESC_CHARS);
		return false;
	}

	return SteamUGC()->SetItemDescription(updateHandle, pDescription);
}

SW_PY bool Workshop_SetItemUpdateLanguage(UGCUpdateHandle_t updateHandle, const char *pLanguage)
{
	return SteamUGC()->SetItemUpdateLanguage(updateHandle, pLanguage);
}

SW_PY bool Workshop_SetItemMetadata(UGCUpdateHandle_t updateHandle, const char *pMetadata)
{
	if (strlen(pMetadata) > UGC_MAX_METADATA_CHARS)
	{
		printf("Metadata cannot have more than %d ASCII characters. Metadata not set.", UGC_MAX_METADATA_CHARS);
	}
	return SteamUGC()->SetItemMetadata(updateHandle, pMetadata);
}

SW_PY bool Workshop_SetItemVisibility(UGCUpdateHandle_t updateHandle, ERemoteStoragePublishedFileVisibility visibility)
{
	return SteamUGC()->SetItemVisibility(updateHandle, visibility);
}

SW_PY bool Workshop_SetItemTags(UGCUpdateHandle_t updateHandle, const char ** stringArray, const int32 stringCount)
{
	SteamParamStringArray_t tags = { stringArray, stringCount };
	
	return SteamUGC()->SetItemTags(updateHandle, &tags);
}

SW_PY bool Workshop_SetItemContent(UGCUpdateHandle_t updateHandle, const char *pContentFolder)
{
	return SteamUGC()->SetItemContent(updateHandle, pContentFolder);
}

SW_PY bool Workshop_SetItemPreview(UGCUpdateHandle_t updateHandle, const char *pPreviewFile)
{
	return SteamUGC()->SetItemPreview(updateHandle, pPreviewFile);
}

SW_PY void Workshop_SetItemUpdatedCallback(SubmitItemUpdateResultCallback_t callback)
{
	workshop.SetItemUpdatedCallback(callback);
}

SW_PY void Workshop_SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *pChangeNote)
{
	workshop.SubmitItemUpdate(updateHandle, pChangeNote);
}

SW_PY EItemUpdateStatus Workshop_GetItemUpdateProgress(UGCUpdateHandle_t handle, uint64 *punBytesProcessed, uint64* punBytesTotal)
{
	return SteamUGC()->GetItemUpdateProgress(handle, punBytesProcessed, punBytesTotal);
}

SW_PY uint32 Workshop_GetNumSubscribedItems()
{
	return SteamUGC()->GetNumSubscribedItems();
}

SW_PY uint32 Workshop_GetSubscribedItems(PublishedFileId_t* pvecPublishedFileID, uint32 maxEntries)
{
	return SteamUGC()->GetSubscribedItems(pvecPublishedFileID, maxEntries);
}

SW_PY uint32 Workshop_GetItemState(PublishedFileId_t publishedFileID)
{
	return SteamUGC()->GetItemState(publishedFileID);
}

SW_PY bool Workshop_GetItemInstallInfo(PublishedFileId_t nPublishedFileID, uint64 *punSizeOnDisk, char *pchFolder, uint32 cchFolderSize, uint32 *punTimeStamp)
{
	return SteamUGC()->GetItemInstallInfo(nPublishedFileID, punSizeOnDisk, pchFolder, cchFolderSize, punTimeStamp);
}

SW_PY bool Workshop_GetItemDownloadInfo(PublishedFileId_t publishedFileID, uint64 *punBytesDownloaded, uint64 *punBytesTotal)
{
	return SteamUGC()->GetItemDownloadInfo(publishedFileID, punBytesDownloaded, punBytesTotal);
}