@echo off
echo [*] Building SteamworksPy

:check_arguments
if %1=="" (
    echo [!] Please call this script with your Visual Studio Version as argument!
    exit /B 5
)
goto setup_environment

:setup_environment
echo [*] Setting up environment
if not exist "C:\Program Files (x86)\Microsoft Visual Studio\%1\BuildTools\Common7\Tools\VsDevCmd.bat" (
    echo [!] Could not find your Visual Studio %1 installation!
    exit /B 5
)
call "C:\Program Files (x86)\Microsoft Visual Studio\%1\BuildTools\Common7\Tools\VsDevCmd.bat" -host_arch=amd64 -arch=amd64
call "C:\Program Files (x86)\Microsoft Visual Studio\%1\BuildTools\Common7\Tools\VsDevCmd.bat" -test
goto check_for_steamworks

:steamworks_missing
echo [!] Your environment is not properly set up!
echo [!] Please follow the instructions in SteamworksPy\library\README.md
exit /B 5

:check_for_steamworks
dir /b /a "library\sdk\steam\*.h" | >nul findstr "^" && (echo [*] SDK available) || (goto steamworks_missing)
if not exist .\library\sdk\redist\steam_api64.dll (
    goto steamworks_missing
)
if not exist .\library\sdk\redist\steam_api64.lib (
    goto steamworks_missing
)
goto main

:main
SET dirname=_build_%random%
echo [*] Building in %dirname%
mkdir %dirname%

echo [*] Copying SteamworksPy.cpp into build root
copy ".\library\SteamworksPy.cpp" ".\%dirname%\SteamworksPy.cpp"

echo [*] Copying Steamworks redist bins to build root
copy ".\library\sdk\redist\*" ".\%dirname%\"

echo [*] Linking SteamworksSDK into build root
mklink /J ".\%dirname%\sdk" ".\library\sdk\"

cd %dirname%

echo [*] Building SteamworksPy.dll
cl.exe /D_USRDLL /D_WINDLL SteamworksPy.cpp steam_api64.lib /link /DLL /OUT:SteamworksPy64.dll

echo [*] Moving finished library into main repo
move "SteamworksPy64.dll" "..\redist\windows\."

cd ..

echo [*] Cleanup
rmdir /S /Q %dirname%
