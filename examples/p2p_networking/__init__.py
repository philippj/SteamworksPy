"""
Example demonstrating Steam P2P networking usage.
"""

import os
import sys
import time

if sys.version_info >= (3, 8):
    os.add_dll_directory(os.getcwd())  # Required since Python 3.8

from steamworks import STEAMWORKS  # Import main STEAMWORKS class

steamworks = STEAMWORKS()
steamworks.initialize()

# Replace with the Steam ID of the remote user you want to connect to
remote_steam_id = 12345678901234567

# Create a P2P session with the remote user
if steamworks.P2PNetworking.CreateP2PSessionWithUser(remote_steam_id):
    print("P2P session created successfully with user:", remote_steam_id)
else:
    print("Failed to create P2P session with user:", remote_steam_id)
    exit(1)

# Send a P2P packet to the remote user
message = "Hello, P2P!"
if steamworks.P2PNetworking.SendP2PPacket(remote_steam_id, message.encode(), len(message), 0):
    print("P2P packet sent successfully to user:", remote_steam_id)
else:
    print("Failed to send P2P packet to user:", remote_steam_id)

# Wait for a P2P packet from the remote user
buffer_size = 1024
buffer = create_string_buffer(buffer_size)
msg_size = c_uint32()
sender_steam_id = c_uint64()

if steamworks.P2PNetworking.ReadP2PPacket(buffer, buffer_size, byref(msg_size), byref(sender_steam_id)):
    received_message = buffer.value[:msg_size.value].decode()
    print("Received P2P packet from user:", sender_steam_id.value)
    print("Message:", received_message)
else:
    print("No P2P packet received")

# Close the P2P session with the remote user
if steamworks.P2PNetworking.CloseP2PSessionWithUser(remote_steam_id):
    print("P2P session closed successfully with user:", remote_steam_id)
else:
    print("Failed to close P2P session with user:", remote_steam_id)
