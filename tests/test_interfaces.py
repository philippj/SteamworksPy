import os, sys
import unittest, psutil

current_path = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_path, '..'))
sys.path.insert(0, project_root)

from steamworks import STEAMWORKS

_steam_running = False
for process in psutil.process_iter():
    if process.name() == 'Steam.exe':
        _steam_running = True
        break

if not _steam_running:
    raise Exception('Steam not running, but required for tests')


class TestCaseInterfaces(unittest.TestCase):
    def setUp(self):
        """
        Sets the steam steam.

        Args:
            self: (todo): write your description
        """
        self.steam = STEAMWORKS()
        self.steam.initialize()

    def test_app_id(self):
        """
        Test if app id is valid.

        Args:
            self: (todo): write your description
        """
        self.assertEqual(self.steam.Utils.GetAppID(), 480)

    def test_app_owner(self):
        """
        Test if app owner.

        Args:
            self: (todo): write your description
        """
        self.assertEqual(self.steam.Apps.GetAppOwner(), self.steam.Users.GetSteamID())