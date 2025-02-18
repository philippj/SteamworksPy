import os
import sys
import unittest
from ctypes import create_string_buffer, c_uint32, byref, c_uint64

current_path = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_path, '..'))
sys.path.insert(0, project_root)

from steamworks import STEAMWORKS

class TestP2PNetworking(unittest.TestCase):
    def setUp(self):
        self.steam = STEAMWORKS()
        self.steam.initialize()

    def test_create_p2p_session(self):
        remote_steam_id = 12345678901234567
        result = self.steam.P2PNetworking.CreateP2PSessionWithUser(remote_steam_id)
        self.assertTrue(result)

    def test_close_p2p_session(self):
        remote_steam_id = 12345678901234567
        self.steam.P2PNetworking.CreateP2PSessionWithUser(remote_steam_id)
        result = self.steam.P2PNetworking.CloseP2PSessionWithUser(remote_steam_id)
        self.assertTrue(result)

    def test_send_p2p_packet(self):
        remote_steam_id = 12345678901234567
        self.steam.P2PNetworking.CreateP2PSessionWithUser(remote_steam_id)
        message = "Hello, P2P!"
        result = self.steam.P2PNetworking.SendP2PPacket(remote_steam_id, message.encode(), len(message), 0)
        self.assertTrue(result)

    def test_receive_p2p_packet(self):
        remote_steam_id = 12345678901234567
        self.steam.P2PNetworking.CreateP2PSessionWithUser(remote_steam_id)
        buffer_size = 1024
        buffer = create_string_buffer(buffer_size)
        msg_size = c_uint32()
        sender_steam_id = c_uint64()
        result = self.steam.P2PNetworking.ReadP2PPacket(buffer, buffer_size, byref(msg_size), byref(sender_steam_id))
        self.assertTrue(result)
        self.assertEqual(sender_steam_id.value, remote_steam_id)
        self.assertEqual(buffer.value[:msg_size.value].decode(), "Hello, P2P!")
