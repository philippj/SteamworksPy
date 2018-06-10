/////////////////////////////////////////////////
/////  STEAMWORKS FOR PYTHON CPP
/////////////////////////////////////////////////
//-----------------------------------------------
//
#include "SteamworksPy.h"
#include "steam/steam_api.h"

Steam::Steam(){
	isInitSuccess = false;
	tickets.clear();
}

CSteamID CreateSteamID(uint32 steamID, int accountType){
	CSteamID cSteamID;
	if(accountType < 0 || accountType >= k_EAccountTypeMax){
		accountType = 1;
	}
	cSteamID.Set(steamID, EUniverse(k_EUniversePublic), EAccountType(accountType));
	return cSteamID;
}
/////////////////////////////////////////////////
///// STEAMWORKS FUNCTIONS //////////////////////
//
// Checks if your executable was launched through Steam and relaunches it through Steam if it wasn't.
bool Steam::RestartAppIfNecessary(int value){
	return SteamAPI_RestartAppIfNecessary((AppId_t)value);
}
// Initialize Steamworks
bool Steam::SteamInit(){
	return SteamAPI_Init();
	// Look for errors
	bool IS_INIT_SUCCESS = SteamAPI_Init();
	int err = FAILED;
	if(IS_INIT_SUCCESS == 1){
		err = OK;
	}
	if(!SteamAPI_IsSteamRunning()){
		err = ERR_NO_CLIENT;
	}
	else if(!SteamUser()->BLoggedOn()){
		err = ERR_NO_CONNECTION;
	}
	if(err == OK && SteamUserStats() != NULL){
		// Load stats and achievements automatically
		SteamUserStats()->RequestCurrentStats();
	}
	return err;
}
// Returns true/false if Steam is running
bool Steam::IsSteamRunning(void){
	return SteamAPI_IsSteamRunning();
}
/////////////////////////////////////////////////
///// APPS //////////////////////////////////////
//
// Check if the user has a given application/game
bool Steam::HasOtherApp(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribedApp((AppId_t)value);
}
// Get the number of DLC the user owns for a parent application/game
int Steam::GetDLCCount(){
	if(SteamApps() == NULL){
		return 0;
	}
	return SteamApps()->GetDLCCount();
}
// Takes AppID of DLC and checks if the user owns the DLC & if the DLC is installed
bool IsDlcInstalled(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsDlcInstalled(value);
}
// Check if given application/game is installed, not necessarily owned
bool IsAppInstalled(int32 value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsAppInstalled((AppId_t)value);
}
// Get the user's game language
const char* GetCurrentGameLanguage(){
	if(SteamApps() == NULL){
		return "None";
	}
	return SteamApps()->GetCurrentGameLanguage();
}
// Does the user have a VAC ban for this game
bool Steam::IsVACBanned(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsVACBanned();
}
// Returns the Unix time of the purchase of the app
int Steam::GetEarliestPurchaseUnixTime(int value){
	if(SteamApps() == NULL){
		return 0;
	}
	return SteamApps()->GetEarliestPurchaseUnixTime((AppId_t)value);
}
// Checks if the user is subscribed to the current app through a free weekend
// This function will return false for users who have a retail or other type of license
// Suggested you contact Valve on how to package and secure your free weekend properly
bool Steam::IsSubscribedFromFreeWeekend(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribedFromFreeWeekend();
}
// Install/Uninstall control for optional DLC
void Steam::InstallDLC(int value){
	if(SteamApps() == NULL){
		return;
	}
	SteamApps()->InstallDLC((AppId_t)value);
}
void Steam::UninstallDLC(int value){
	if(SteamApps() == NULL){
		return;
	}
	SteamApps()->UninstallDLC((AppId_t)value);
}
// Is subscribed lacks notes
bool Steam::IsSubscribed(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribed();
}
// Presumably if Steam is set to low violence; lacks note
bool Steam::IsLowViolence(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsLowViolence();
}
// Presumably if users is a cyber cafe; lacks notes
bool Steam::IsCybercafe(){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsCybercafe();
}
// Only use to check ownership of another game related to yours: a demo, etc.
bool Steam::IsSubscribedApp(int value){
	if(SteamApps() == NULL){
		return false;
	}
	return SteamApps()->BIsSubscribedApp((AppId_t)value);
}
// Return the build ID for this app; will change based on backend updates
int Steam::GetAppBuildId(){
	if(SteamApps() == NULL){
		return 0;
	}
	return SteamApps()->GetAppBuildId();
}
/////////////////////////////////////////////////
///// FRIENDS ///////////////////////////////////
//
// Get number of friends user has
int Steam::GetFriendCount(){
	if(SteamFriends() == NULL){
		return 0;
	}
	return SteamFriends()->GetFriendCount(0x04);
}
// Get the user's Steam username
const char* Steam::GetPersonaName(){
	if(SteamFriends() == NULL){
		return "";
	}
	return SteamFriends()->GetPersonaName();
}
// Get given friend's Steam username
const char* Steam::GetFriendPersonaName(int steamID){
	if(SteamFriends() != NULL && steamID > 0){
		CSteamID friendID = CreateSteamID(steamID);
		bool isDataLoading = SteamFriends()->RequestUserInformation(friendID, true);
		if(!isDataLoading){
			return SteamFriends()->GetFriendPersonaName(friendID);
		}
	}
	return "";
}
// Set the game information in Steam; used in 'View Game Info'
void Steam::SetGameInfo(const char* key, const char* value){
	// Rich presence data is automatically shared between friends in the same game
	// Each user has a set of key/value pairs, up to 20 can be set
	// Two magic keys (status, connect)
	// setGameInfo() to an empty string deletes the key
	if(SteamFriends() == NULL){
		return;
	}
	SteamFriends()->SetRichPresence(key, value);
}
// Clear the game information in Steam; used in 'View Game Info'
void Steam::ClearGameInfo(){
	if(SteamFriends() == NULL){
		return;
	}
	SteamFriends()->ClearRichPresence();
}
// Invite friend to current game/lobby
void Steam::InviteFriend(int steamID, const char* connectString){
	if(SteamFriends() == NULL){
		return;
	}
	CSteamID friendID = CreateSteamID(steamID);
	SteamFriends()->InviteUserToGame(friendID, connectString);
}
// Set player as 'Played With' for game
void Steam::SetPlayedWith(int steamID){
	if(SteamFriends() == NULL){
		return;
	}
	CSteamID friendID = CreateSteamID(steamID);
	SteamFriends()->SetPlayedWith(friendID);
}
// Get player's avatar
void Steam::GetFriendAvatar(int size){
	if(size < AVATAR_SMALL || size > AVATAR_LARGE){
		return;
	}
	if(SteamFriends() == NULL){
		return;
	}
	int handle = -2;
	switch(size){
		case AVATAR_SMALL:{
			handle = SteamFriends()->GetSmallFriendAvatar( SteamUser()->GetSteamID() );
			size = 32; break;
		}
		case AVATAR_MEDIUM:{
			handle = SteamFriends()->GetMediumFriendAvatar( SteamUser()->GetSteamID() );
			size = 64; break;
		}
		case AVATAR_LARGE:{
			handle = SteamFriends()->GetLargeFriendAvatar( SteamUser()->GetSteamID() );
			size = 184; break;
		}
		default:
			return;
	}
	if(handle <= 0){
		if(handle == -1){
			// Still loading
			return;
		}
		// Invalid
		return;
	}
	// Has already loaded, simulate callback
	AvatarImageLoaded_t* avatarData = new AvatarImageLoaded_t;
	avatarData->m_steamID = SteamUser()->GetSteamID();
	avatarData->m_iImage = handle;
	avatarData->m_iWide = size;
	avatarData->m_iTall = size;
	_avatar_loaded(avatarData);
	delete avatarData;
	return;
}
// Draw the given avatar
//TEXTURE Steam::DrawAvatar(int image){
//	TEXTURE texture = 0;
//	uint32 avatarWidth, avatarHeight;
//	bool success SteamUtils()->GetImageSize(image, avatarWidth, avatarHeight);
//	if(!success){
//		return texture;
//	}
//	// Get the raw RGBA data from Steam and do something with it
//	const int imageSize = avatarWidth * avatarHeight * 4;
//	uint8 *avatarRGBA = new uint8[imageSize];
//	success = SteamUtils()->GetImageRGBA(image, avatarRGBA, imageSize);
//	if(!success){
//		Do something to conert texture
//	}
//	delete[] avatarRGBA;
//	return texture;
//}
// Activates the overlay with optional dialog to open the following: "Friends", "Community", "Players", "Settings", "OfficialGameGroup", "Stats", "Achievements", "LobbyInvite"
void Steam::ActivateGameOverlay(const char* url){
	if(SteamFriends() == NULL){
		return;
	}
	SteamFriends()->ActivateGameOverlay(url);
}
// Activates the overlay to the following: "steamid", "chat", "jointrade", "stats", "achievements", "friendadd", "friendremove", "friendrequestaccept", "friendrequestignore"
void Steam::ActivateGameOverlayToUser(const char* url, int steam_id){
	if(SteamFriends() == NULL){
		return;
	}
	CSteamID overlayUserID = CreateSteamID(steam_id);
	SteamFriends()->ActivateGameOverlayToUser(url, overlayUserID);
}
// Activates the overlay with specified web address
void Steam::ActivateGameOverlayToWebPage(const char* url){
	if(SteamFriends() == NULL){
		return;
	}
	SteamFriends()->ActivateGameOverlayToWebPage(url);
}
// Activates the overlay with the application/game Steam store page
void Steam::ActivateGameOverlayToStore(int app_id){
	if(SteamFriends() == NULL){
		return;
	}
	SteamFriends()->ActivateGameOverlayToStore(AppId_t(app_id), EOverlayToStoreFlag(0));
}
// Activates game overlay to open the invite dialog. Invitations will be sent for the provided lobby
void Steam::ActivateGameOverlayInviteDialog(int steam_id){
	if(SteamFriends() == NULL){
		return;
	}
	CSteamID lobbyID = CreateSteamID(steam_id);
	SteamFriends()->ActivateGameOverlayInviteDialog(lobbyID);
}
/////////////////////////////////////////////////
///// MATCHMAKING ///////////////////////////////
//
// Create a lobby on the Steam servers, if private the lobby will not be returned by any RequestLobbyList() call
void Steam::CreateLobby(int lobbyType, int maxMembers){
	if(SteamMatchmaking() == NULL){
		return;
	}
	ELobbyType eLobbyType;
	// Convert the lobby type back over
	if(lobbyType == PRIVATE){
		eLobbyType = k_ELobbyTypePrivate;
	}
	else if(lobbyType == FRIENDS_ONLY){
		eLobbyType = k_ELobbyTypeFriendsOnly;
	}
	else if(lobbyType == PUBLIC){
		eLobbyType = k_ELobbyTypePublic;	
	}
	else{
		eLobbyType = k_ELobbyTypeInvisible;
	}
	SteamMatchmaking()->CreateLobby(eLobbyType, maxMembers);
}
// Join an existing lobby
void Steam::JoinLobby(int steamIDLobby){
	if(SteamMatchmaking() == NULL){
		return;
	}
	CSteamID lobbyID = CreateSteamID(steamIDLobby);
	SteamMatchmaking()->JoinLobby(lobbyID);
}
// Leave a lobby, this will take effect immediately on the client side, other users will be notified by LobbyChatUpdate_t callback
void Steam::LeaveLobby(int steamIDLobby){
	if(SteamMatchmaking() == NULL){
		return;
	}
	CSteamID lobbyID = CreateSteamID(steamIDLobby);
	return SteamMatchmaking()->LeaveLobby(lobbyID);
}
// Invite another user to the lobby, the target user will receive a LobbyInvite_t callback, will return true if the invite is successfully sent, whether or not the target responds
bool Steam::InviteUserToLobby(int steamIDLobby, int steamIDInvitee){
	if(SteamMatchmaking() == NULL){
		return 0;
	}
	CSteamID lobbyID = CreateSteamID(steamIDLobby);
	CSteamID inviteeID = CreateSteamID(steamIDInvitee);
	return SteamMatchmaking()->InviteUserToLobby(lobbyID, inviteeID);
}
/////////////////////////////////////////////////
///// MUSIC /////////////////////////////////////
//
// Is Steam music enabled
bool Steam::MusicIsEnabled(){
	if(SteamMusic() == NULL){
		return false;
	}
	return SteamMusic()->BIsEnabled();
}
// Is Steam music playing something
bool Steam::MusicIsPlaying(){
	if(SteamMusic() == NULL){
		return false;
	}
	return SteamMusic()->BIsPlaying();
}
// Get the volume level of the music
float Steam::MusicGetVolume(){
	if(SteamMusic() == NULL){
		return 0;
	}
	return SteamMusic()->GetVolume();
}
// Pause whatever Steam music is playing
void Steam::MusicPause(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->Pause();
}
// Play current track/album
void Steam::MusicPlay(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->Play();
}
// Play next track/album
void Steam::MusicPlayNext(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->PlayNext();
}
// Play previous track/album
void Steam::MusicPlayPrev(){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->PlayPrevious();
}
// Set the volume of Steam music
void Steam::MusicSetVolume(float value){
	if(SteamMusic() == NULL){
		return;
	}
	return SteamMusic()->SetVolume(value);
}
/////////////////////////////////////////////////
///// REMOTE STORAGE ////////////////////////////
//
// Write to given file from Steam Cloud
//bool Steam::FileWrite(const char* file, const void *data, int32 dataSize){
//	if(SteamRemoteStorage() == NULL){
//		return false;
//	}
//	return SteamRemoteStorage()->FileWrite(file, data, dataSize);
//}
// Read given file from Steam Cloud
//int32 Steam::FileRead(const char* file, void *data, int32 dataToRead){
//	if(SteamRemoteStorage() == NULL){
//		return false;
//	}
//	vector<uint8> data;
//	data.resize(dataToRead);
//	Dictionary d;
//	d["ret"] = SteamRemoteStorage()->FileRead(file, Data.write().ptr(), dataToRead);
//	d["buf"] = data;
//	return d;
//}
// Delete file from remote storage but leave it on local disk to remain accessible
bool Steam::FileForget(const char* file){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->FileForget(file);
}
// Delete a given file in Steam Cloud
bool Steam::FileDelete(const char* file){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->FileDelete(file);
}
// Check if a given file exists in Steam Cloud
bool Steam::FileExists(const char* file){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->FileExists(file);
}
// Check if a given file is persisted in Steam Cloud
bool Steam::FilePersisted(const char* file){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->FilePersisted(file);
}
// Get the size of a given file
int32 Steam::GetFileSize(const char* file){
	if(SteamRemoteStorage() == NULL){
		return -1;
	}
	return SteamRemoteStorage()->GetFileSize(file);
}
// Get the timestamp of when the file was uploaded/changed
int64 Steam::GetFileTimestamp(const char* file){
	if(SteamRemoteStorage() == NULL){
		return -1;
	}
	return SteamRemoteStorage()->GetFileTimestamp(file);
}
// Gets the total number of local files synchronized by Steam Cloud
int32 Steam::GetFileCount(){
	if(SteamRemoteStorage() == NULL){
		return 0;
	}
	return SteamRemoteStorage()->GetFileCount();
}
// Is Steam Cloud enabled on the user's account?
bool Steam::IsCloudEnabledForAccount(){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->IsCloudEnabledForAccount();
}
// Is Steam Cloud enabled for this application?
bool Steam::IsCloudEnabledForApp(){
	if(SteamRemoteStorage() == NULL){
		return false;
	}
	return SteamRemoteStorage()->IsCloudEnabledForApp();
}
// Set Steam Cloud enabled for this application
void Steam::SetCloudEnabledForApp(bool enabled){
	if(SteamRemoteStorage() == NULL){
		return;
	}
	return SteamRemoteStorage()->SetCloudEnabledForApp(enabled);
}
// Gets the file name and size of a file from the index
//map Steam::GetFileNameAndSize(int file){
//	map d;
//	const char name = "";
//	int32 size = 0;
//	if(SteamRemoteStorage() != NULL){
//		name = const char(SteamRemoteStorage()->GetFileNameAndSize(file, &size));
//	}
//	d["name"] = name;
//	d["size"] = size;
//	return d;
//}
// Gets the number of bytes available, and used on the users Steam Cloud storage
//map Steam::GetQuota(){
//	map d;
//	uint64 total = 0;
//	uint64 available = 0;
//	if(SteamRemoteStorage() != NULL){
//		SteamRemoteStorage()->GetQuota((uint64*)&total, (uint64*)&available);
//	}
//	d["total_bytes"] = total;
//	d["available_bytes"] = available;
//	return d;
//}
// Obtains the platforms that the specified file will syncronize to
uint32 Steam::GetSyncPlatforms(const char* file){
	if(SteamRemoteStorage() == NULL){
		return 0;
	}
	return SteamRemoteStorage()->GetSyncPlatforms(file);
}
/////////////////////////////////////////////////
///// SCREENSHOTS ///////////////////////////////
//
// Toggles whether the overlay handles screenshots
void Steam::HookScreenshots(bool hook){
	if(SteamScreenshots() == NULL){
		return;
	}
	SteamScreenshots()->HookScreenshots(hook);
}
// Checks if the app is hooking screenshots
bool Steam::IsScreenshotsHooked(){
	if(SteamScreenshots() == NULL){
		return false;
	}
	return SteamScreenshots()->IsScreenshotsHooked();
}
// Causes Steam overlay to take a screenshot
void Steam::TriggerScreenshot(){
	if(SteamScreenshots() == NULL){
		return;
	}
	SteamScreenshots()->TriggerScreenshot();
}
// Writes a screenshot to the user's Steam screenshot library
//uint32 Steam::WriteScreenshot(const map<uint8_t>& RGB, int width, int height){
//	if(SteamScreenshots() == NULL){
//		return 0;
//	}
//	return SteamScreenshots()->WriteScreenshot((void*)RGB.read().ptr(), RGB.size(), width, height);
//}
/////////////////////////////////////////////////
///// USERS /////////////////////////////////////
//
// Get an authentication ticket
//uint32 Steam::GetAuthSessionTicket(){
//	if(SteamUser() == NULL){
//		return 0;
//	}
//	uint32 cbTicket = 1024;
//	uint32 *buf = memnew_arr(uint32, cbTicket);
//	uint32 id = SteamUser()->GetAuthSessionTicket(buf, cbTicket, &cbTicket);
//	TicketData ticket = { id, buf, cbTicket };
//	tickets.push_back(ticket);
//	return id;
//}
// Cancels an auth ticket
//void Steam::CancelAuthTicket(uint32 authTicket){
//	if(SteamUser() == NULL){
//		return;
//	}
//	for(int i=0; i<tickets.size(); i++){
//		TicketData ticket = tickets.get(i);
//		if (ticket.id == authTicket){
//			tickets.remove(i);
//			memdelete_arr(ticket.buf);
//			break;
//		}
//	}
//}
// Authenticate the ticket from the entity Steam ID to be sure it is valid and isn't reused
//int Steam::BeginAuthSession(uint32 authTicket, uint64 steamID){
//	if(SteamUser() == NULL){
//		return -1;
//	}
//	for(int i=0; i<tickets.size(); i++){
//		TicketData ticket = tickets.get(i);
//		if (ticket.id == authTicket){
//			CSteamID authSteamID = CreateSteamID(steamID);
//			return SteamUser()->BeginAuthSession(ticket.buf, ticket.size, authSteamID);
//		}
//	}
//	return -1;
//}
// Ends an auth session
void Steam::EndAuthSession(uint64 steamID){
	if(SteamUser() == NULL){
		return;
	}
	CSteamID authSteamID = CreateSteamID(steamID);
	return SteamUser()->EndAuthSession(authSteamID);
}
// Get user's Steam ID
uint64 Steam::GetSteamID(){
	if(SteamUser() == NULL){
		return 0;
	}
	CSteamID cSteamID = SteamUser()->GetSteamID();
	return cSteamID.ConvertToUint64();
}
// Check, true/false, if user is logged into Steam currently
bool Steam::LoggedOn(){
	if(SteamUser() == NULL){
		return false;
	}
	return SteamUser()->BLoggedOn();
}
// Get the user's Steam level
int Steam::GetPlayerSteamLevel(){
	if(SteamUser() == NULL){
		return 0;
	}
	return SteamUser()->GetPlayerSteamLevel(); 
}
// Get the user's Steam installation path
//const char Steam::GetUserDataFolder(){
//	if(SteamUser() == NULL){
//		return "";
//	}
//	const int cubBuffer = 256;
//	char *pchBuffer = new char[cubBuffer];
//	SteamUser()->GetUserDataFolder((char*)pchBuffer, cubBuffer);
//	const char data_path = pchBuffer;
//	delete pchBuffer;
//	return data_path;
//}
// (LEGACY FUNCTION) Set data to be replicated to friends so that they can join your game
//void Steam::AdvertiseGame(const char* serverIP, int port){
//	if(SteamUser() == NULL){
//		return;
//	}
//	CSteamID gameserverID = SteamUser()->GetSteamID();
//	SteamUser()->AdvertiseGame(gameserverID, *((uint32 *)serverIP), port);
//}
// Trading Card badges data access, if you only have one set of cards, the series will be 1
// The user has can have two different badges for a series; the regular (max level 5) and the foil (max level 1)
int Steam::GetGameBadgeLevel(int series, bool foil){
	if(SteamUser()== NULL){
		return 0;
	}
	return SteamUser()->GetGameBadgeLevel(series, foil);
}
/////////////////////////////////////////////////
///// USER STATS ////////////////////////////////
//
// Clears a given achievement
bool Steam::ClearAchievement(const char* name){
	return SteamUserStats()->ClearAchievement(name);
}
// Return true/false if use has given achievement
bool Steam::GetAchievement(const char* name){
	bool achieved = false;
	SteamUserStats()->GetAchievement(name, &achieved);
	return achieved;
}
// Returns the percentage of users who have unlocked the specified achievement
//map Steam::GetAchievementAchievedPercent(const char* name){
//	map d;
//	float percent = 0.f;
//	bool achieved = false;
//	if(SteamUserStats() == NULL){
//		d["ret"] = false;
//	} else {
//		d["ret"] = SteamUserStats()->GetAchievementAchievedPercent(name, &percent);
//	}
//	d["percent"] = percent;
//	return d;
//}
//  Get the amount of players currently playing the current game (online + offline)
void Steam::GetNumberOfCurrentPlayers(){
	if(SteamUserStats() == NULL){
		return;
	}
	SteamAPICall_t apiCall = SteamUserStats()->GetNumberOfCurrentPlayers();
	callResultNumberOfCurrentPlayers.Set(apiCall, this, &Steam::_number_of_current_players);
}
// Get the number of achievements
uint32 Steam::GetNumAchievements(){
	if(SteamUserStats() == NULL){
		return 0;
	}
	return SteamUserStats()->GetNumAchievements();
}
// Get the value of a float statistic
float Steam::GetStatFloat(const char* name){
	float statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
// Get the value of an integer statistic
int Steam::GetStatInt(const char* name){
	int32 statval = 0;
	SteamUserStats()->GetStat(name, &statval);
	return statval;
}
// Reset all Steam statistics; optional to reset achievements
bool Steam::ResetAllStats(bool achievementsToo){
	SteamUserStats()->ResetAllStats(achievementsToo);
	return SteamUserStats()->StoreStats();
}
// Request all statistics and achievements from Steam servers
bool Steam::RequestCurrentStats(){
	return SteamUserStats()->RequestCurrentStats();
}
// Asynchronously fetch the data for the percentages
//void Steam::RequestGlobalAchievementPercentages(){
//	if(SteamUserStats() == NULL){
//		return;
//	}
//	SteamAPICall_t apiCall = SteamUserStats()->RequestGlobalAchievementPercentages();
//	callResultGlobalAchievementPercentagesReady.Set(apiCall, this, &Steam::_global_achievement_percentages_ready);
//}
// Set a given achievement
bool Steam::SetAchievement(const char* name){
	if(SteamUserStats() == NULL){
		return 0;
	}
	SteamUserStats()->SetAchievement(name);
	return SteamUserStats()->StoreStats();
}
// Set a float statistic
bool Steam::SetStatFloat(const char* name, float value){
	return SteamUserStats()->SetStat(name, value);
}
// Set an integer statistic
bool Steam::SetStatInt(const char* name, int value){
	return SteamUserStats()->SetStat(name, value);
}
// Store all statistics, and achievements, on Steam servers; must be called to "pop" achievements
bool Steam::StoreStats(){
	if(SteamUserStats() == NULL){
		return 0;
	}
	SteamUserStats()->StoreStats();
	return SteamUserStats()->RequestCurrentStats();
}
// Find a given leaderboard, by name
//void Steam::FindLeaderboard(const char* name){
//	if(SteamUserStats() == NULL){
//		return;
//	}
//	//SteamAPICall_t apiCall = 
//	SteamUserStats()->FindLeaderboard(name);
//}
// Get the name of a leaderboard
//const char Steam::GetLeaderboardName(){
//	if(SteamUserStats() == NULL){
//		return "";
//	}
//	return SteamUserStats()->GetLeaderboardName(leaderboard_handle);
//}
// Get the total number of entries in a leaderboard, as of the last request
//int Steam::GetLeaderboardEntryCount(){
//	if(SteamUserStats() == NULL){
//		return -1;
//	}
//	return SteamUserStats()->GetLeaderboardEntryCount(leaderboard_handle);
//}
// Request all rows for friends of user
//void Steam::DownloadLeaderboardEntries(int start, int end, int type){
//	if(SteamUserStats() == NULL){
//		return;
//	}
//	//SteamAPICall_t apiCall = 
//	SteamUserStats()->DownloadLeaderboardEntries(leaderboard_handle, ELeaderboardDataRequest(type), start, end);
//}
// Request a maximum of 100 users with only one outstanding call at a time
//void Steam::DownloadLeaderboardEntriesForUsers(int usersID[]){
//	if(SteamUserStats() == NULL){
//		return;
//	}
//	int users_count = usersID.size();
//	if(users_count == 0){
//		return;
//	}
//	CSteamID *pUsers = new CSteamID[users_count];
//	for(int i = 0; i < users_count; i++){
//		CSteamID user = CreateSteamID(usersID[i]);
//		pUsers[i] = user;
//	}
//	SteamUserStats()->DownloadLeaderboardEntriesForUsers(leaderboard_handle, pUsers, users_count);
//	delete[] pUsers;
//}
// Upload a leaderboard score for the user
//void Steam::UploadLeaderboardScore(int score, bool keepBest){
//	if(SteamUserStats() == NULL){
//		return;
//	}
//	ELeaderboardUploadScoreMethod method = keepBest ? k_ELeaderboardUploadScoreMethodKeepBest : k_ELeaderboardUploadScoreMethodForceUpdate;
//	SteamAPICall_t apiCall = SteamUserStats()->UploadLeaderboardScore(leaderboard_handle, method, (int32)score, NULL, 0);
//	callResultUploadScore.Set(apiCall, this, &Steam::_leaderboard_uploaded);
//}
// Once all entries are accessed, the data will be freed up and the handle will become invalid, use this to store it
//bool Steam::GetDownloadedLeaderboardEntry(SteamLeaderboardEntries_t handle, int entryCount){
//	if(SteamUserStats() == NULL){
//		return 0;
//	}
//	leaderboard_entries.clear();
//	LeaderboardEntry_t *entry = new(LeaderboardEntry_t);
//	for(int i = 0; i < entryCount; i++){
//		SteamUserStats()->GetDownloadedLeaderboardEntry(handle, i, entry, NULL, 0);
//		const char entryDict;
//		entryDict["score"] = entry->m_nScore;
//		entryDict["steam_id"] = entry->m_steamIDUser.GetAccountID();
//		entryDict["global_rank"] = entry->m_nGlobalRank;
//		leaderboard_entries.append(entryDict);
//	}
//	delete(entry);
//}
// Get the currently used leaderboard handle
uint64 Steam::GetLeaderboardHandle(){
	return leaderboard_handle;
}
// Get the currently used leaderboard entries
const char* Steam::GetLeaderboardEntries(){
	return leaderboard_entries;
}
// Get the achievement status, and the time it was unlocked if unlocked (in seconds since January 1, 19)
bool Steam::GetAchievementAndUnlockTime(const char *name, bool *achieved, uint32 *unlockTime){
	if(SteamUserStats() == NULL){
		return 0;
	}
	return SteamUserStats()->GetAchievementAndUnlockTime(name, (bool *)achieved, (uint32 *)unlockTime);
}
// Achievement progress, triggers an AchievementProgress callback, that is all.
// Calling this with X out of X progress will NOT set the achievement, the game must still do that.
bool Steam::IndicateAchievementProgress(const char *name, uint32 currentProgress, uint32 maxProgress){
	if(SteamUserStats() == NULL){
		return 0;
	}
	return SteamUserStats()->IndicateAchievementProgress(name, currentProgress, maxProgress);
}
/////////////////////////////////////////////////
///// UTILS /////////////////////////////////////
//
// Get the user's country by IP
const char* Steam::GetIPCountry(){
	return SteamUtils()->GetIPCountry();
}
// Returns true/false if Steam overlay is enabled
bool Steam::IsOverlayEnabled(){
	return SteamUtils()->IsOverlayEnabled();
}
// Set the position where overlay shows notifications
void Steam::SetOverlayNotificationPosition(int pos){
	if((pos < 0) || (pos > 3) || (SteamUtils() == NULL)){
		return;
	}
	SteamUtils()->SetOverlayNotificationPosition(ENotificationPosition(pos));
}
// Get the Steam user interface language
const char* Steam::GetSteamUILanguage(){
	return SteamUtils()->GetSteamUILanguage();
}
// Get the Steam ID of the running application/game
int Steam::GetAppID(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetAppID();
}
// Return amount of time, in seconds, user has spent in this session
int Steam::GetSecondsSinceAppActive(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetSecondsSinceAppActive();
}
// Get the amount of battery power, clearly for laptops
int Steam::GetCurrentBatteryPower(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetCurrentBatteryPower();
}
// Is Steam running in VR?
bool Steam::IsSteamRunningInVR(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->IsSteamRunningInVR();
}
// Get the actual time
int Steam::GetServerRealTime(){
	if(SteamUtils() == NULL){
		return 0;
	}
	return SteamUtils()->GetServerRealTime();
}
// Returns true if Steam & the Steam Overlay are running in Big Picture mode
bool Steam::IsSteamInBigPictureMode(){
	if(SteamUtils() == NULL){
		return false;
	}
	return SteamUtils()->IsSteamInBigPictureMode();
}
// Ask SteamUI to create and render its OpenVR dashboard
void Steam::StartVRDashboard(){
	if(SteamUtils() == NULL){
		return;
	}
	SteamUtils()->StartVRDashboard();
}
/////////////////////////////////////////////////
///// WORKSHOP //////////////////////////////////
//
// Download new or update already installed item. If returns true, wait for DownloadItemResult_t. If item is already installed, then files on disk should not be used until callback received.
// If item is not subscribed to, it will be cached for some time. If bHighPriority is set, any other item download will be suspended and this item downloaded ASAP.
bool Steam::DownloadItem(int publishedFileID, bool highPriority){
	if(SteamUGC() == NULL){
		return 0;
	}
	PublishedFileId_t fileID = (int)publishedFileID;
	return SteamUGC()->DownloadItem(fileID, highPriority);
}
// SuspendDownloads( true ) will suspend all workshop downloads until SuspendDownloads( false ) is called or the game ends.
void Steam::SuspendDownloads(bool suspend){
	return SteamUGC()->SuspendDownloads(suspend);
}
// Starts the item update process.
uint64 Steam::StartItemUpdate(AppId_t appID, int publishedFileID){
	PublishedFileId_t fileID = (int)publishedFileID;
	return SteamUGC()->StartItemUpdate(appID, fileID);
}
// Gets the current state of a workshop item on this client.
int Steam::GetItemState(int publishedFileID){
	if(SteamUGC() == NULL){
		return 0;
	}
	PublishedFileId_t fileID = (int)publishedFileID;
	return SteamUGC()->GetItemState(fileID);
}
// Gets the progress of an item update.
int Steam::GetItemUpdateProgress(UGCUpdateHandle_t updateHandle, uint64 *bytesProcessed, uint64* bytesTotal){
	return SteamUGC()->GetItemUpdateProgress(updateHandle, (uint64*)&bytesProcessed, bytesTotal);
}
//
void Steam::CreateItem(AppId_t appID, EWorkshopFileType fileType){
	if(SteamUGC() == NULL){
		return;
	}
	SteamAPICall_t apiCall = SteamUGC()->CreateItem(appID, fileType);
	callResultItemCreate.Set(apiCall, this, &Steam::_workshop_item_created);
}
// Sets a new title for an item.
bool Steam::SetItemTitle(UGCUpdateHandle_t updateHandle, const char *title){
	if(SteamUGC() == NULL){
		return false;
	}
	if (strlen(title) > UGC_MAX_TITLE_CHARS){
		printf("Title cannot have more than %d ASCII characters. Title not set.", UGC_MAX_TITLE_CHARS);
		return false;
	}
	return SteamUGC()->SetItemTitle(updateHandle, title);
}
// Sets a new description for an item.
bool Steam::SetItemDescription(UGCUpdateHandle_t updateHandle, const char *description){
	if(SteamUGC() == NULL){
		return false;
	}
	if(strlen(description) > UGC_MAX_DESC_CHARS){
		printf("Description cannot have more than %d ASCII characters. Description not set.", UGC_MAX_DESC_CHARS);
		return false;
	}
	return SteamUGC()->SetItemDescription(updateHandle, description);
}
// Sets the language of the title and description that will be set in this item update.
bool Steam::SetItemUpdateLanguage(UGCUpdateHandle_t updateHandle, const char *language){
	if(SteamUGC() == NULL){
		return false;
	}
	return SteamUGC()->SetItemUpdateLanguage(updateHandle, language);
}
// Sets arbitrary metadata for an item. This metadata can be returned from queries without having to download and install the actual content.
bool Steam::SetItemMetadata(UGCUpdateHandle_t updateHandle, const char *metadata){
	if(SteamUGC() == NULL){
		return false;
	}
	if(strlen(metadata) > UGC_MAX_METADATA_CHARS){
		printf("Metadata cannot have more than %d ASCII characters. Metadata not set.", UGC_MAX_METADATA_CHARS);
	}
	return SteamUGC()->SetItemMetadata(updateHandle, metadata);
}
// Sets the visibility of an item.
bool Steam::SetItemVisibility(UGCUpdateHandle_t updateHandle, ERemoteStoragePublishedFileVisibility visibility){
	if(SteamUGC() == NULL){
		return false;
	}
	return SteamUGC()->SetItemVisibility(updateHandle, visibility);
}
// Sets arbitrary developer specified tags on an item.
bool Steam::SetItemTags(UGCUpdateHandle_t updateHandle, const SteamParamStringArray_t *tags){
	if(SteamUGC() == NULL){
		return false;
	}
	return SteamUGC()->SetItemTags(updateHandle, tags);
}
// Sets the folder that will be stored as the content for an item.
bool Steam::SetItemContent(UGCUpdateHandle_t updateHandle, const char *contentFolder){
	if(SteamUGC() == NULL){
		return false;
	}
	return SteamUGC()->SetItemContent(updateHandle, contentFolder);
}
// Sets the primary preview image for the item.
bool Steam::SetItemPreview(UGCUpdateHandle_t updateHandle, const char *previewFile){
	if(SteamUGC() == NULL){
		return false;
	}
	return SteamUGC()->SetItemPreview(updateHandle, previewFile);
}
// Uploads the changes made to an item to the Steam Workshop; to be called after setting your changes.
void Steam::SubmitItemUpdate(UGCUpdateHandle_t updateHandle, const char *changeNote){
	if(SteamUGC() == NULL){
		return;
	}
	SteamAPICall_t apiCall = SteamUGC()->SubmitItemUpdate(updateHandle, changeNote);
	callResultItemUpdate.Set(apiCall, this, &Steam::_workshop_item_updated);
}
uint32 Steam::GetSubscribedItems(PublishedFileId_t* publishedFileID, uint32 maxEntries){
	if(SteamUGC() == NULL){
		return 0;
	}
	return SteamUGC()->GetSubscribedItems(publishedFileID, maxEntries);
}
// Gets info about currently installed content on the disc for workshop items that have k_EItemStateInstalled set.
bool Steam::GetItemInstallInfo(int publishedFileID, uint64 *sizeOnDisk, char *folder, uint32 folderSize, uint32 *timeStamp){
	if(SteamUGC() == NULL){
		return false;
	}
	PublishedFileId_t fileID = (int)publishedFileID;
	return SteamUGC()->GetItemInstallInfo(fileID, sizeOnDisk, folder, folderSize, timeStamp);
}
// Get info about a pending download of a workshop item that has k_EItemStateNeedsUpdate set.
bool Steam::GetItemDownloadInfo(int publishedFileID, uint64 *bytesDownloaded, uint64 *bytesTotal){
	if(SteamUGC() == NULL){
		return false;
	}
	PublishedFileId_t fileID = int(publishedFileID);
	return SteamUGC()->GetItemDownloadInfo(fileID, bytesDownloaded, bytesTotal);
}

Steam::~Steam(){
	if(isInitSuccess){
		SteamUserStats()->StoreStats();
		SteamAPI_Shutdown;
	}
	for(int i = 0; i < tickets.size(); i++){
		TicketData ticket = tickets.at(i);
		delete ticket.buffer;
	}
	tickets.clear();
}