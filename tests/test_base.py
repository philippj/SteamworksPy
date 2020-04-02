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


class TestCaseSTEAMWORKS(unittest.TestCase):
    def setUp(self):
        self.steam = STEAMWORKS()
        self.steam.initialize()

    def test_populated(self):
        for interface in ['Apps', 'Friends', 'Matchmaking', 'Music', 'Screenshots', 'Users', 'UserStats', 'Utils', \
                          'Workshop']:
            self.assertTrue((hasattr(self.steam, interface) and getattr(self.steam, interface) is not None))
