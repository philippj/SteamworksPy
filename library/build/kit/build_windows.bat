call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\Common7\Tools\VsDevCmd.bat" -host_arch=amd64 -arch=amd64
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\Common7\Tools\VsDevCmd.bat" -test

dir

SET dirname=_build_%random%
echo "Building in %dirname%"
mkdir %dirname%

echo "Copying SteamworksPy.cpp into build root"
copy "SteamworksPy.cpp" ".\%dirname%\SteamworksPy.cpp"

echo "Copying Steamworks redist bins to build root"
copy ".\build\steamworks\redist\*" ".\%dirname%\"

echo "Linking SteamworksSDK into build root"
mklink /J ".\%dirname%\steam" ".\build\steamworks\steam"

cd %dirname%

echo "Contents of build root"
dir

echo "Building SteamworksPy.dll"
cl /D_USRDLL /D_WINDLL SteamworksPy.cpp steam_api64.lib /link /DLL /OUT:SteamworksPy64.dll

echo "Moving finished library into main repo"
move "SteamworksPy64.dll" "..\..\."

cd ..

echo "Cleanup"
rmdir /S /Q %dirname%

cd ..
dir