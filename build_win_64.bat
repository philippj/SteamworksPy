@echo off
echo [*] Building SteamworksPy

:check_arguments
if "%1"=="" (
    echo [!] Please call this script with your Visual Studio Version as an argument!
    exit /B 5
)
goto setup_environment

:setup_environment
echo [*] Setting up environment
set VS_PATH="C:\Program Files (x86)\Microsoft Visual Studio\%1\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not exist %VS_PATH% (
    echo [!] Could not find your Visual Studio %1 installation!
    exit /B 5
)

call %VS_PATH%
goto check_for_steamworks

:steamworks_missing
echo [!] Your environment is not properly set up!
echo [!] Please follow the instructions in SteamworksPy\library\README.md
exit /B 5

:check_for_steamworks
if not exist "library\sdk\steam\*.h" goto steamworks_missing
if not exist "library\sdk\redist\steam_api64.dll" goto steamworks_missing
if not exist "library\sdk\redist\steam_api64.lib" goto steamworks_missing

goto main

:main
SET dirname=_build_%random%
echo [*] Building in %dirname%
mkdir %dirname%

echo [*] Copying SteamworksPy.cpp into build root
copy ".\library\SteamworksPy.cpp" ".\%dirname%\SteamworksPy.cpp"

echo [*] Copying Steamworks redist bins to build root
copy ".\library\sdk\redist\*" ".\%dirname%\"

echo [*] Linking SteamworksSDK into build root (Requires Admin!)
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [!] This script requires administrator privileges for mklink!
    exit /B 5
)
mklink /J ".\%dirname%\sdk" ".\library\sdk\"

cd %dirname%

echo [*] Building SteamworksPy.dll
cl.exe /D_USRDLL /D_WINDLL SteamworksPy.cpp steam_api64.lib /link /DLL /OUT:SteamworksPy64.dll
if %errorLevel% NEQ 0 (
    echo [!] Compilation failed!
    exit /B 5
)

echo [*] Moving finished library into main repo
move "SteamworksPy64.dll" "..\redist\windows\."

cd ..

echo [*] Cleanup
rmdir /S /Q %dirname%

echo [*] Build completed successfully!
exit /B 0
