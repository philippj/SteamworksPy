//SteamPy

#include <steam/steam_api.h>
#include <steam/isteamfriends.h>
#include <steam/isteamugc.h>

extern "C"
{
	__declspec(dllexport) bool SteamInit();
	__declspec(dllexport) const char* GetPersonaName();
	__declspec(dllexport) int GetFriendCount();
	__declspec(dllexport) const char* GetFriendNameByIndex(int index, int flag);
	__declspec(dllexport) int GetFriendStateByIndex(int index, int flag);
	__declspec(dllexport) int GetPersonaState();
	__declspec(dllexport) uint32 GetFriendGame(int index, int flag);
	__declspec(dllexport) bool IsFriendInGame(int index, int flag);
	__declspec(dllexport) void SetPersonaName(const char* newname);
}
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