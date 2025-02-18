from steamworks.exceptions import SteamNotLoadedException


class SteamP2PNetworking:
    def __init__(self, steam: object):
        self.steam = steam
        if not self.steam.loaded():
            raise SteamNotLoadedException('STEAMWORKS not yet loaded')

    def CreateP2PSessionWithUser(self, steam_id_remote: int) -> bool:
        return self.steam.CreateP2PSessionWithUser(steam_id_remote)

    def CloseP2PSessionWithUser(self, steam_id_remote: int) -> bool:
        return self.steam.CloseP2PSessionWithUser(steam_id_remote)

    def SendP2PPacket(self, steam_id_remote: int, data: bytes, data_size: int, send_type: int) -> bool:
        return self.steam.SendP2PPacket(steam_id_remote, data, data_size, send_type)

    def ReadP2PPacket(self, buffer: bytes, buffer_size: int, msg_size: int, sender_steam_id: int) -> bool:
        return self.steam.ReadP2PPacket(buffer, buffer_size, msg_size, sender_steam_id)
