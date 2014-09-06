//SteamPy

#include <steam/steam_api.h>
#include <steam/isteamfriends.h>
#include <steam/isteamugc.h>

#if defined _WIN32
	extern "C"
	{
		DLL_PUBLIC bool SteamInit();
		DLL_PUBLIC const char* GetPersonaName();
		DLL_PUBLIC int GetFriendCount();
		DLL_PUBLIC const char* GetFriendNameByIndex(int index, int flag);
		DLL_PUBLIC int GetFriendStateByIndex(int index, int flag);
		DLL_PUBLIC int GetPersonaState();
		DLL_PUBLIC uint32 GetFriendGame(int index, int flag);
		DLL_PUBLIC bool IsFriendInGame(int index, int flag);
		DLL_PUBLIC void SetPersonaName(const char* newname);
	}
#else
	bool SteamInit();
	const char* GetPersonaName();
	int GetFriendCount();
	const char* GetFriendNameByIndex(int index, int flag);
	int GetFriendStateByIndex(int index, int flag);
	int GetPersonaState();
	uint32 GetFriendGame(int index, int flag);
	bool IsFriendInGame(int index, int flag);
	void SetPersonaName(const char* newname);
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
