#include <steam/steam_api.h>

bool SteamInit();
const char* GetPersonaName();
int GetFriendCount();
const char* GetFriendNameByIndex(int index, int flag);
int GetFriendStateByIndex(int index, int flag);
int GetPersonaState();
uint32 GetFriendGame(int index, int flag);
bool IsFriendInGame(int index, int flag);
void SetPersonaName(const char* newname);