//SteamPy

#include <steam/steam_api.h>
#include <steam/isteamfriends.h>
#include <steam/isteamugc.h>
#include <steam/isteamutils.h>

#if defined _WIN32
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
		
	}
#else
	//Steam
	__attribute__ ((visibility ("default"))) bool SteamInit(void);
	//SteamFriends
	__attribute__ ((visibility ("default"))) const char* GetPersonaName(void);
	__attribute__ ((visibility ("default"))) int GetFriendCount(void);
	__attribute__ ((visibility ("default"))) const char* GetFriendNameByIndex(int index, int flag);
	__attribute__ ((visibility ("default"))) int GetFriendStateByIndex(int index, int flag);
	__attribute__ ((visibility ("default"))) int GetPersonaState(void);
	__attribute__ ((visibility ("default"))) uint32 GetFriendGame(int index, int flag);
	__attribute__ ((visibility ("default"))) bool IsFriendInGame(int index, int flag);
	__attribute__ ((visibility ("default"))) void SetPersonaName(const char* newname);
	//SteamUtils
	__attribute__ ((visibility ("default"))) bool IsOverlayEnabled(void);
	__attribute__ ((visibility ("default"))) uint8 GetCurrentBatteryPower(void);
	__attribute__ ((visibility ("default"))) uint32 GetSecondsSinceAppActive(void);
	__attribute__ ((visibility ("default"))) uint32 GetSecondsSinceComputerActive(void);
	__attribute__ ((visibility ("default"))) uint32 GetServerRealTime(void);
	__attribute__ ((visibility ("default"))) const char* GetIPCountry();
	__attribute__ ((visibility ("default"))) bool IsSteamRunningInVR();
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