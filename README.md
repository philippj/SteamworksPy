# SteamworksForPython
Howdy!  This is a branch of Easimer's SteamworksForPython in an attempt to bring a fully-functional Python module for Steam out for the public.

Feel free to fork or contribute to this module.

For a fuller tutorial, with images, on SteamworksPy please read our post: http://coaguco.tumblr.com/post/128240756897/steamworks-for-python-tutorial-linux.

# Some Notes
While I am still tinkering away with this, here are some things to note:

- You will need the Steamworks SDK
- You will most likely need a Steamworks account, with a valid AppID, to use more advanced functions (set achievements, set stats, etc.)
- You will need to be logged into Steam for anything to function, obviously.  As it assumes the game is run from Steam itself and is online.
- Steam Overlay will only work if your game is using OpenGL or D3D!  Overlay will only work if the game is actually launched from Steam itself.  Possible if the SteamRestart command is fired; however, this is not implemented yet in SteamworksPy.

# To Do
- Add in more features from the Steamworks SDK
- Create a Mac version (I do not own a Mac, so someone who does that can help out would be greatly appreciated!)
- Add features/function updates for UGC and Workshop additions from peacegiverman

# How To
1. Download this repo and unpack
2. Download and unpack the Steamworks SDK
3. Move the Steam header (steam) folder from /sdk/public/ into the unpacked repo for compiling
4. Move the Steam API file from /sdk/redistributable_bin into the unpacked repo
  - For Linux, find libsteam_api.so
      - This file might need to be copied to /usr/lib for the compiling to work if Steam does not copy it correctly
  - For Windows, find steam_api.dll or steam_api64.dll as well as steam_api.lib or steam_api64.lib
5. Create the new DLL or SO file
  - For Linux:
    - Run the makefile from the repo
    - Alternately, you could just run something like:
    ```
    g++ -std=c++11 -o SteamworksPy.so -shared -fPIC SteamworksPy.cpp -l steam_api -L
    ```
  - For Windows:
    - Create a new DLL project in Visual Studio
    - New > Project
    - Templates > Visual C++ > Win32 > Win32 Project
    - Follow the wizard and pick the DLL Application Type
    - Add SteamworksPy.cpp to Source Files and steam_api.h from /steam/ folder to Header Files
    - Go to Project > Properties in the toolbar
    - Under C/C++ > Precompiled Headers, turn off Precompiled Header option
    - Under Linker > Input, add steam_api.lib or steam_api64.lib to Additional Dependenices
    - Clean and build
6. Move the steamworks.py and new compiled SteamworkPy.so or SteamworksPy.dll from the unpacked repo into your project
  - You also will have to move over the libsteam_api.so or steam_api.dll as well
7. Add the following to your to your main file or whichever file you plan on calling Steam from:
```
from steamworks import *
#Initialize Steam
Steam.Init()
```
From here you should be able to call various functions of the steamworks.py.  A list of available functions is listed below; take a closer look at the steamworks.py for a better understanding.  In addition, you should be able to read the Steamworks API documentation to see what all is available and cross-reference with the steamworks.py!

# Features / Functions
1. Init()
  - Starts up the Steam API
2. GetDLCCount()
  - Get the total number of DLC installed for this game
3. IsDlcInstalled()
  - Is a particular DLC installed for this game
  - You must pass the DLC's AppID
4. RequestAppProofOfPurchaseKey()
  - Should return the game's serial number, if it exists
5. GetFriendCount()
  - Get the number of friends the user has
6. GetPlayerName()
  - Get the user's name
7. GetPersonaState()
  - Get the user's current state
8. ActivateGameOverlay()
  - This should activate the Steam Overlay
  - Useful for binding keys to
9. MusicIsEnabled()
  - Check whether or not Steam Music is enabled
10. MusicIsPlaying()
  - Is Steam Music currently playing something?
11. MusicGetVolume()
  - Get the system's current volume level
12. MusicPause()
  - Pause whatever Steam Music is playing currently
13. MusicPlay()
  - Play whatever track Steam Music is on
14. MusicPlayNext()
  - Play the next track in Steam Music
15. MusicPlayPrevious()
  - Play the previous track in Steam Music
16. MusicSetVolume()
  - Set the system's volume
  - Must pass a float between 0.0 and 1.0
17. GetPlayerID()
  - Get the user's Steam ID number
  - Currently just returns 0
18. GetPlayerSteamLevel()
  - Should return the user's Steam level
19. ClearAchievement()
  - Clear the specified achievement from the user
  - Must pass achievement's name in Steam (eg. STEAM_ACHIEVE_1)
20. GetAchievement()
  - Find whether or not the specified achievement is earned
  - Must pass achievement's name in Steam (eg. STEAM_ACHIEVE_1)
21. GetStatFloat()
  - Get value of specified float statistic
  - Must pass statistic's name in Steam (eg. TOTAL_GAMES)
22. GetStatInt()
  - Get value of specified integer statistic
  - Must pass statistic's name in Steam (eg. TOTAL_GAMES)
23. ResetAllStats()
  - Resets all of the user's statistics, perhaps also achievements
24. RequestCurrentStats()
  - Pulls all of the user's statistics and achievements
  - Should be called before calling any Get stats/achievement functions
25. SetAchievement()
  - Set a particular achievement for the user
  - Must pass achievement's name in Steam (eg. STEAM_ACHIEVE_1)
26. SetStat()
  - Set a particular statistic for the user; either INT or FLOAT
  - Must pass statistics's name and value in Steam (eg. TOTAL_GAMES, 4)
27. StoreStats()
  - Sends all the statistics and achievements to Steam servers
28. GetCurrentBatteryPower()
  - Get the user's battery power level
29. GetIPCountry()
  - Get the two-digit code for the user's IP address
30. GetSecondsSinceAppActive()
  - Get the number of seconds since the game started up
31. GetSecondsSinceComputerActive()
  - Get the number of seconds since the user's computer was started
32. GetServerRealTime()
  - Get the time from the server, probably
33. IsOverlayEnabled()
  - Is the Steam overlay enabled
34. IsSteamRunningInVR()
  - Is Steam's VR service running
35. GetSteamUILanguage()
  - Gets the user's Steam UI language (eg. English, French, etc.)
36. GetAppID()
  - Should return the game's App ID

# Further Usage
I recommend trying the included tests to get an idea of how it works. Opening the test files will give you some insight on how to use it in your game, as well as looking through the Steamworks.py file itself.  Also, don't hesitate to contact me for help or with questions. Or comment / open issue on GitHub.

# More To Come
I am still digging through the code and trying to get more functions working.  Some things like controller might not be necessary as Python can usually handle these; though they may have more to do with the new Steam Controller.
