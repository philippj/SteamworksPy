//===============================================
//  STEAMWORKS FOR PYTHON
//===============================================

// Modify SW_PY based on operating system and include the proper Steamworks API file
//-----------------------------------------------
#if defined( _WIN32 )
	#include "steam\steam_api.h"
	#define SW_PY __declspec( dllexport )
#elif defined( __APPLE__ )
	#include "steam/steam_api.h"
	#include "TargetConditionals.h"
	#define SW_PY __attribute__ ((visibility("default")))
#elif defined( __linux__ )
	#include "steam/steam_api.h"
	#define SW_PY __attribute__ ((visibility("default")))
#else
	#error "Unsupported platform"
#endif

#include <functional> 

// Steamworks functions
//-----------------------------------------------
extern "C" SW_PY bool SteamInit(void){
	return SteamAPI_Init();
}
extern "C" SW_PY bool IsSteamRunning(void){
	return SteamAPI_IsSteamRunning();
}
// Steam Apps
extern "C" SW_PY int GetDlcCount(){
	return SteamApps()->GetDLCCount();
}
extern "C" SW_PY bool IsDlcInstalled(int32 value){
	return SteamApps()->BIsDlcInstalled(value);
}
extern "C" SW_PY void RequestAppProofOfPurchaseKey(int32 value){
	return SteamApps()->RequestAppProofOfPurchaseKey(value);
}
// Steam Friends
extern "C" SW_PY int GetFriendCount(int flag){
	return SteamFriends()->GetFriendCount(flag);
}
extern "C" SW_PY const char* GetPersonaName(){
	return SteamFriends()->GetPersonaName();
}
extern "C" SW_PY int GetPersonaState(){
	return SteamFriends()->GetPersonaState();
}
extern "C" SW_PY void ActivateGameOverlay(const char* name){
	return SteamFriends()->ActivateGameOverlay(name);	
}
// Steam Music
extern "C" SW_PY bool MusicIsEnabled(){
	return SteamMusic()->BIsEnabled();
}
extern "C" SW_PY bool MusicIsPlaying(){
	return SteamMusic()->BIsPlaying();
}
extern "C" SW_PY float MusicGetVolume(){
	return SteamMusic()->GetVolume();
}
extern "C" SW_PY void MusicPause(){
	return SteamMusic()->Pause();
}
extern "C" SW_PY void MusicPlay(){
	return SteamMusic()->Play();
}
extern "C" SW_PY void MusicPlayNext(){
	return SteamMusic()->PlayNext();
}
extern "C" SW_PY void MusicPlayPrev(){
	return SteamMusic()->PlayPrevious();
}
extern "C" SW_PY void MusicSetVolume(float value){
	return SteamMusic()->SetVolume(value);
}
// Steam User
extern "C" SW_PY CSteamID GetSteamID(){
	return SteamUser()->GetSteamID();
}
extern "C" SW_PY int GetPlayerSteamLevel(){
	return SteamUser()->GetPlayerSteamLevel(); 
}
// Steam User Stats
extern "C" SW_PY bool ClearAchievement(const char* name){
	return SteamUserStats()->ClearAchievement(name);
}
extern "C" SW_PY bool GetAchievement(const char* name){
	bool achieved = false;
	SteamUserStats()->GetAchievement(name, &achieved);
	return achieved;
}
extern "C" SW_PY float GetStatFloat(const char* name){
	float statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
extern "C" SW_PY int32 GetStatInt(const char* name){
	int32 statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
extern "C" SW_PY bool ResetAllStats(bool achievesToo){
	return SteamUserStats()->ResetAllStats(achievesToo);
}
extern "C" SW_PY bool RequestCurrentStats(){
	return SteamUserStats()->RequestCurrentStats();
}
extern "C" SW_PY bool SetAchievement(const char* name){
	return SteamUserStats()->SetAchievement(name);
}
extern "C" SW_PY bool SetStatFloat(const char* name, float value){
	return SteamUserStats()->SetStat(name, value);
}
extern "C" SW_PY bool SetStatInt(const char* name, int32 value){
	return SteamUserStats()->SetStat(name, value);
}
extern "C" SW_PY bool StoreStats(){
	return SteamUserStats()->StoreStats();
}
// Steam Utilities
extern "C" SW_PY uint8 GetCurrentBatteryPower(){
	return SteamUtils()->GetCurrentBatteryPower();
}
extern "C" SW_PY const char* GetIPCountry(){
	const char* c_ptr = SteamUtils()->GetIPCountry();
	printf("SteamworksPy: %s", c_ptr);

	return c_ptr;
}
extern "C" SW_PY uint32 GetSecondsSinceAppActive(){
	return SteamUtils()->GetSecondsSinceAppActive();
}
extern "C" SW_PY uint32 GetSecondsSinceComputerActive(){
	return SteamUtils()->GetSecondsSinceComputerActive();
}
extern "C" SW_PY uint32 GetServerRealTime(){
	return SteamUtils()->GetServerRealTime();
}
extern "C" SW_PY bool IsOverlayEnabled(){
	return SteamUtils()->IsOverlayEnabled();
}
extern "C" SW_PY bool IsSteamRunningInVR(){
	return SteamUtils()->IsSteamRunningInVR();
}
extern "C" SW_PY const char* GetSteamUILanguage(){
	return SteamUtils()->GetSteamUILanguage();
}
extern "C" SW_PY uint32 GetAppID(){
	return SteamUtils()->GetAppID();
}

class Workshop
{
public:
	void (*workshopItemCreatedCallback)(CreateItemResult_t);

	_declspec(dllexport) void SetWorkshopItemCreatedCallback(void(*callback)(CreateItemResult_t))
	{
		workshopItemCreatedCallback = callback;
	}
	
	// Steam UGC (Workshop)
	_declspec( dllexport ) void CreateItem(AppId_t consumerAppId, EWorkshopFileType fileType, void(*callback)(CreateItemResult_t) = NULL)
	{
		//TODO: Check if fileType is a valid value?

		if (&callback != NULL) {
			SetWorkshopItemCreatedCallback(callback);
		}

		SteamUGC()->CreateItem(consumerAppId, fileType);
	}

private:
	STEAM_CALLBACK(Workshop, OnWorkshopItemCreated, CreateItemResult_t);

	void OnWorkshopItemCreated(CreateItemResult_t createItemResult)
	{
		workshopItemCreatedCallback(createItemResult);
	}
};