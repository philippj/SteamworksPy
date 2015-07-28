# SteamworksForPython
Howdy!  This is a branch of Easimer's SteamworksForPython in an attempt to bring a fully-functional Python module for Steam out for the public.

Feel free to fork or contribute to this module.

# Some Notes
While I am still tinkering away with this, here are some things to note:

- You will need the Steamworks SDK
- You will most likely need a Steamworks account, with a valid AppID, to use more advanced functions (set achievements, set stats, etc.)
- You will need to be logged into Steam for anything to function, obviously.  As it assumes the game is run from Steam itself and is online.

# To Do
- Get steampy.dll compiled on Windows
- Add in additional features like getting Steam ID of user, clearing statistics, matchmaking, etc.

# How To (Linux)
1. Download and unpacked the Steamworks SDK
  - In Linux, I have placed it in the home folder
2. Download this repo and unpack it inside the Steamworks SDK
  - Place it in /sdk/public/
3. On Linux, run make and it should create the libsteampy.so
  - This file has now been included so it does not need to be compiled (uses Steamworks 1.33b)
4. Place the libsteampy.so, steamworks.py in your project's folder
  - These files must be together unless you modify the steamworks.py to find the libsteampy.so
5. Like the examples, add this to your project main file:
```
from steamworks import *
#Initialize Steam
Steam.Init()
```
From here you should be able to call various functions of the steamworks.py; use the steamworks.py to see what you can call from your Python project.

# Advanced Features
1. Achievements
  - Setting achievements does not seem to work. Original testing wasn't thorough enough as the achievements were setting based on statistics saved in Steam not calls sent to it from the client.  This may only be failing based on the way it is set up, but currently it does not seem to work for me.
2. Statistics
  - Calling SteamUserStats.SetStat(STAT-NAME, STAT-VALUE) will set the Steam statistic appropriately. STAT-NAME needs to be whatever was set for your statistic in Steamworks, obviously. This will push the value to Steam, which should be handled mainly by your game and only stored on Steam when needed.
3. Getting User Statistics
  - Calling SteamUserStats.RequestCurrentStats seems to respond with False. Steam should respond with True when the data is ready.  However, pulling data seems to work okay regardless.
  - Calling SteamUserStats.GetAhievement(ACHIEVEMENT-NAME) will respond with True if the user has this achievement unlocked or not.
  - Calling SteamUserStats.GetStatInt(STAT-NAME) or SteamUserStats.GetStatFloat(STAT-NAME) will respond with the corresponding value stored on Steam's servers.

# More To Come
I am still digging through the code and trying to get more functions like setting achievements and stats, but these definitely require a Steamworks account and AppID.  Without your game on Steam, I don't think you can really use those functions but I haven't actually tested it yet.  I will update more later, especially the Windows how-to as I have not spent time on it.

One thing I wish this library did do was procure the user's Steam ID.  It will pull the name, but that can be changed by the user at will and isn't a good way to keep track of users outside of Steam itself.  This can be achieved by adding more functions into the steampy.cpp for compiling.  There are actually a LOT more functions not implemented in here yet.
