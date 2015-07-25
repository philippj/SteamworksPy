//SteamPy
// Modified for compiling from within Steamworks SDK
//#include <steam/steam_api.h>
//#include <steam/isteamfriends.h>
//#include <steam/isteamugc.h>
//#include <steam/isteamutils.h>
//#include <steam/isteammusic.h>
//#include <steam/isteamuserstats.h>
#include "steam/steam_api.h"
#include "steam/isteamfriends.h"
#include "steam/isteamugc.h"
#include "steam/isteamutils.h"
#include "steam/isteammusic.h"
#include "steam/isteamuserstats.h"

#if defined(_WIN32)
	extern "C"
	{
		//Steam
		__declspec(dllexport) bool SteamInit(void);
		//SteamFriends
		__declspec(dllexport) const char* GetPersonaName(void);
		__declspec(dllexport) int GetFriendCount(void);
		__declspec(dllexport) const char* GetFriendNameByIndex(int index, int flag);
		__declspec(dllexport) int GetFriendStateByIndex(int index, int flag);
		__declspec(dllexport) int GetPersonaState(void);
		__declspec(dllexport) uint32 GetFriendGame(int index, int flag);
		__declspec(dllexport) bool IsFriendInGame(int index, int flag);
		__declspec(dllexport) void SetPersonaName(const char* newname);
		//SteamUtils
		__declspec(dllexport) uint32 GetSecondsSinceAppActive(void);
		__declspec(dllexport) uint32 GetSecondsSinceComputerActive(void);
		__declspec(dllexport) bool IsOverlayEnabled(void);
		__declspec(dllexport) uint8 GetCurrentBatteryPower(void);
		__declspec(dllexport) uint32 GetServerRealTime(void);
		__declspec(dllexport) const char* GetIPCountry();
		__declspec(dllexport) bool IsSteamRunningInVR();
		//SteamMusic
		__declspec(dllexport) bool MusicIsEnabled(void);
		__declspec(dllexport) bool MusicIsPlaying(void);
		__declspec(dllexport) void MusicPlay(void);
		__declspec(dllexport) void MusicPause(void);
		__declspec(dllexport) void MusicPlayNext(void);
		__declspec(dllexport) void MusicPlayPrev(void);
		__declspec(dllexport) void MusicSetVolume(float vol);
		__declspec(dllexport) float MusicGetVolume(void);
		//SteamUserStats
        __declspec(dllexport) int32* GetStatInt(const char* name);
        __declspec(dllexport) float* GetStatFloat(const char* name);
        __declspec(dllexport) bool SetStatInt(const char* name, int32 value);
        __declspec(dllexport) bool SetStatFloat(const char* name, float value);
        __declspec(dllexport) bool StoreStats();
        __declspec(dllexport) bool RequestCurrentStats();
        __declspec(dllexport) bool* GetAchievement(const char* name);
        __declspec(dllexport) bool SetAchievement(const char* name);
	}
#elif __linux__
    extern "C"
	{
	   //Steam
	   __attribute__((__visibility__("default"))) bool SteamInit(void);
	   //SteamFriends
        __attribute__((__visibility__("default"))) const char* GetPersonaName(void);
        __attribute__((__visibility__("default"))) int GetFriendCount(void);
	   __attribute__((__visibility__("default"))) const char* GetFriendNameByIndex(int index, int flag);
        __attribute__((__visibility__("default"))) int GetFriendStateByIndex(int index, int flag);
	   __attribute__((__visibility__("default"))) int GetPersonaState(void);
        __attribute__((__visibility__("default"))) uint32 GetFriendGame(int index, int flag);
        __attribute__((__visibility__("default"))) bool IsFriendInGame(int index, int flag);
	   __attribute__((__visibility__("default"))) void SetPersonaName(const char* newname);
        //SteamUtils
	   __attribute__((__visibility__("default"))) bool IsOverlayEnabled(void);
        __attribute__((__visibility__("default"))) uint8 GetCurrentBatteryPower(void);
        __attribute__((__visibility__("default"))) uint32 GetSecondsSinceAppActive(void);
        __attribute__((__visibility__("default"))) uint32 GetSecondsSinceComputerActive(void);
	   __attribute__((__visibility__("default"))) uint32 GetServerRealTime(void);
        __attribute__((__visibility__("default"))) const char* GetIPCountry();
	   __attribute__((__visibility__("default"))) bool IsSteamRunningInVR();
	   //Steam Music
		__attribute__((__visibility__("default"))) bool MusicIsEnabled(void);
		__attribute__((__visibility__("default"))) bool MusicIsPlaying(void);
		__attribute__((__visibility__("default"))) void MusicPlay(void);
		__attribute__((__visibility__("default"))) void MusicPause(void);
		__attribute__((__visibility__("default"))) void MusicPlayNext(void);
		__attribute__((__visibility__("default"))) void MusicPlayPrev(void);
		__attribute__((__visibility__("default"))) void MusicSetVolume(float vol);
		__attribute__((__visibility__("default"))) float MusicGetVolume(void);
        //SteamUserStats
        __attribute__((__visibility__("default"))) int32 GetStatInt(const char* name);
        __attribute__((__visibility__("default"))) float GetStatFloat(const char* name);
        __attribute__((__visibility__("default"))) bool SetStatInt(const char* name, int32 value);
        __attribute__((__visibility__("default"))) bool SetStatFloat(const char* name, float value);
        __attribute__((__visibility__("default"))) bool StoreStats();
        __attribute__((__visibility__("default"))) bool RequestCurrentStats();
        __attribute__((__visibility__("default"))) bool GetAchievement(const char* name);
        __attribute__((__visibility__("default"))) bool SetAchievement(const char* name);
    }
#else
	#error "Unsupported platform"
#endif

bool SteamInit()
{
	return SteamAPI_Init();
}

const char* GetPersonaName()
{
	return SteamFriends()->GetPersonaName();
}

int GetFriendCount(int flag)
{
	return SteamFriends()->GetFriendCount(flag);
}

const char* GetFriendNameByIndex(int index, int flag)
{
	const char* name = SteamFriends()->GetFriendPersonaName(SteamFriends()->GetFriendByIndex(index, flag));
	return name;
}

int GetFriendStateByIndex(int index, int flag)
{
	return SteamFriends()->GetFriendPersonaState(SteamFriends()->GetFriendByIndex(index, flag));
}

int GetPersonaState()
{
	return SteamFriends()->GetPersonaState();
}

uint32 GetFriendGame(int index, int flag)
{
	FriendGameInfo_t* friendgame = new FriendGameInfo_t();
	SteamFriends()->GetFriendGamePlayed(SteamFriends()->GetFriendByIndex(index, flag), friendgame);
	return friendgame->m_gameID.AppID();
}

bool IsFriendInGame(int index, int flag)
{
	return SteamFriends()->GetFriendGamePlayed(SteamFriends()->GetFriendByIndex(index, flag), new FriendGameInfo_t());
}

void SetPersonaName(const char* newname)
{
	SteamFriends()->SetPersonaName(newname);
}

bool IsOverlayEnabled()
{
	return SteamUtils()->IsOverlayEnabled();
}

uint8 GetCurrentBatteryPower()
{
	return SteamUtils()->GetCurrentBatteryPower();
}

const char* GetIPCountry()
{
	return SteamUtils()->GetIPCountry();
}

uint32 GetSecondsSinceAppActive()
{
	return SteamUtils()->GetSecondsSinceAppActive();
}

uint32 GetSecondsSinceComputerActive()
{
	return SteamUtils()->GetSecondsSinceComputerActive();
}

uint32 GetServerRealTime()
{
	return SteamUtils()->GetServerRealTime();
}

bool IsSteamRunningInVR()
{
	return SteamUtils()->IsSteamRunningInVR();
}

//Steam Music

bool MusicIsEnabled()
{
	return SteamMusic()->BIsEnabled();
}

bool MusicIsPlaying()
{
	return SteamMusic()->BIsPlaying();
}

void MusicPlay()
{
	return SteamMusic()->Play();
}

void MusicPause()
{
	return SteamMusic()->Pause();
}

float MusicGetVolume()
{
	return SteamMusic()->GetVolume();
}

void MusicSetVolume(float vol)
{
	return SteamMusic()->SetVolume(vol);
}

void MusicPlayPrev()
{
	return SteamMusic()->PlayPrevious();
}

void MusicPlayNext()
{
	return SteamMusic()->PlayNext();
}

int32 GetStatInt(const char* name)
{
	int32 statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}

float GetStatFloat(const char* name)
{
	float statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}

bool SetStatInt(const char* name, int32 value)
{
	return SteamUserStats()->SetStat(name, value);
}

bool SetStatFloat(const char* name, float value)
{
	return SteamUserStats()->SetStat(name, value);
}

bool StoreStats()
{
	return SteamUserStats()->StoreStats();
}

bool RequestCurrentStats()
{
	return SteamUserStats()->RequestCurrentStats();
}

bool GetAchievement(const char* name)
{
	bool achieved = false;
	SteamUserStats()->GetAchievement(name, &achieved);
	return achieved;
}

bool SetAchievement(const char* name)
{
	return SteamUserStats()->SetAchievement(name);
}
