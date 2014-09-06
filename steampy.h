#include <steam/steam_api.h>

//Steam
bool SteamInit(void);
//SteamFriends
const char* GetPersonaName(void);
int GetFriendCount(void);
const char* GetFriendNameByIndex(int index, int flag);
int GetFriendStateByIndex(int index, int flag);
int GetPersonaState(void);
uint32 GetFriendGame(int index, int flag);
bool IsFriendInGame(int index, int flag);
void SetPersonaName(const char* newname);
//SteamUtils
bool IsOverlayEnabled(void);
uint8 GetCurrentBatteryPower(void);
uint32 GetSecondsSinceAppActive(void);
uint32 GetSecondsSinceComputerActive(void);
uint32 GetServerRealTime(void);