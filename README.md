# SteamworksPy
Howdy!  This project originally started as a fork of Easimer's SteamworksForPython in an attempt to bring a fully-functional Python module for Steam out for the public.  Since then it has grown beyond that and added a lot of functionality.

Feel free to fork or contribute to this module.

Pre-builds for Windows and Linux here: https://github.com/Gramps/SteamworksPy/releases

Full documentation is now available here: https://gramps.github.io/SteamworksPy/

For a fuller (yet outdated) tutorial, with images, on SteamworksPy please read our post: http://coaguco.tumblr.com/post/128240756897/steamworks-for-python-tutorial-linux.

There is now an experimental branch for converting the project to match my [Godot Engine module](https://github.com/Gramps/GodotSteam) in functionality and fix some problems with the original.  Once completed, it will move to the master branch.

# Requirements
Following files are required to be located in your project working directory:
- steam_appid.txt - Stating your games app id or any other valid app id given the account owns a license
- steam_api library (.dll, .so, .darwin) and the corresponding steam_api.lib
- SteamworksPy library (.dll, .so, .darwin)

The library will only function if the Steam client is running and logged in. Otherwise you will encounter exceptions.

# Some Notes
While I am still tinkering away with this, here are some things to note:

- You will need a Steamworks account, with a valid AppID, to use more advanced functions (set achievements, set stats, etc.)
- Steam Overlay will only work if your game is using OpenGL or D3D!  Overlay will only work if the game is actually launched from Steam itself.  Possible if the SteamRestart command is fired; however, this is not implemented yet in SteamworksPy.

# Usage
Please check the examples in the "examples" directory for a basic understanding of the module. For further reference you can go through the interface implementations itself or use the official Steamworks documentation (https://partner.steamgames.com/doc/api)
