//SteamPy

#include <steam/steam_api.h>
#include <steam/isteamfriends.h>
#include <steam/isteamugc.h>
#include <steam/isteamutils.h>
#include <steam/isteammusic.h>

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
		//Steam Music
		__declspec(dllexport) bool MusicIsEnabled(void);
		__declspec(dllexport) bool MusicIsPlaying(void);
		__declspec(dllexport) void MusicPlay(void);
		__declspec(dllexport) void MusicPause(void);
		__declspec(dllexport) void MusicPlayNext(void);
		__declspec(dllexport) void MusicPlayPrev(void);
		__declspec(dllexport) void MusicSetVolume(float vol);
		__declspec(dllexport) float MusicGetVolume(void);
	}
#elif defined(GNUC) || defined(COMPILER_GCC)
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