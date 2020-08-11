# SteamworksPy
Howdy!  This project originally started as a fork of Easimer's SteamworksForPython in an attempt to bring a fully-functional Python module for Steam out for the public.  Since then it has grown beyond that and added a lot of functionality.

Feel free to fork or contribute to this module.

Pre-builds for Windows and Linux here: https://github.com/philippj/SteamworksPy/releases

Full documentation on getting started is now available here: https://philippj.github.io/SteamworksPy/

## What's New
Updates since February 1st, 2020
- Added: GetNumAchievements, GetAchievementName, GetAChievementDisplayAttribute by **aveao**
- Added: missing file for packaging by **tpchanho**
- Changed: organized Apps and Friends functions alphabetically to make editing easier
- Changed: ClearGameInfo to actual Steamworks function ClearRichPresence
- Fixed: argtypes for Workshop_SuspendDownloads by **tpchanho**

## Requirements
Following files are required to be located in your project working directory:
- steam_appid.txt - Stating your games app id or any other valid app id given the account owns a license
- steam_api library (.dll, .so, .darwin) and the corresponding steam_api.lib
- SteamworksPy library (.dll, .so, .darwin)

The library will only function if the Steam client is running and logged in. Otherwise you will encounter exceptions.

## Some Notes
While I am still tinkering away with this, here are some things to note:

- You will need a Steamworks account, with a valid AppID, to use more advanced functions (set achievements, set stats, etc.)
- Steam Overlay will only work if your game is using OpenGL or D3D!  Overlay will only work if the game is actually launched from Steam itself.  Possible if the SteamRestart command is fired; however, this is not implemented yet in SteamworksPy.
- Do not install Python from the Microsoft App Store. Make sure to [download and install it from Python's main site.](https://www.python.org/)

## Usage
Please check the examples in the "examples" directory for a basic understanding of the module. For further reference you can go through the interface implementations itself or use the official Steamworks documentation (https://partner.steamgames.com/doc/api)
