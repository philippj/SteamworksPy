from ctypes import *
from enum import Enum

import steamworks.util 		as util
from steamworks.enums 		import *
from steamworks.structs 	import *
from steamworks.exceptions 	import *


class SteamWorkshop(object):
    _CreateItemResult_t 		= CFUNCTYPE(None, CreateItemResult_t)
    _SubmitItemUpdateResult_t 	= CFUNCTYPE(None, SubmitItemUpdateResult_t)
    _ItemInstalled_t 			= CFUNCTYPE(None, ItemInstalled_t)
    _RemoteStorageSubscribePublishedFileResult_t 	= CFUNCTYPE(None, RemoteStorageSubscribePublishedFileResult_t)
    _RemoteStorageUnubscribePublishedFileResult_t 	= CFUNCTYPE(None, RemoteStorageUnubscribePublishedFileResult_t)

    _CreateItemResult			= None
    _SubmitItemUpdateResult 	= None
    _ItemInstalled 				= None
    _RemoteStorageSubscribePublishedFileResult 	= None
    _RemoteStorageUnubscribePublishedFileResult = None


    def __init__(self, steam: object):
        self.steam = steam
        if not self.steam.loaded():
            raise SteamNotLoadedException('STEAMWORKS not yet loaded')


    def SetItemCreatedCallback(self, callback: object) -> bool:
        """Set callback for item created

        :param callback: callable
        :return: bool
        """
        self._CreateItemResult = SteamWorkshop._CreateItemResult_t(callback)
        self.steam._cdll.Workshop_SetItemCreatedCallback(self._CreateItemResult)
        return True


    def SetItemUpdatedCallback(self, callback: object) -> bool:
        """Set callback for item updated

        :param callback: callable
        :return: bool
        """
        self._SubmitItemUpdateResult = self._SubmitItemUpdateResult_t(callback)
        self.steam._cdll.Workshop_SetItemUpdatedCallback(self._SubmitItemUpdateResult)
        return True


    def SetItemInstalledCallback(self, callback: object) -> bool:
        """Set callback for item installed

        :param callback: callable
        :return: bool
        """
        self._ItemInstalled = self._ItemInstalled_t(callback)
        self.steam._cdll.Workshop_SetItemInstalledCallback(self._ItemInstalled)
        return True


    def ClearItemInstalledCallback(self) -> None:
        """Clear item installed callback

        :return: None
        """
        self._ItemInstalled = None
        self.steam._cdll.Workshop_ClearItemInstalledCallback()


    def SetItemSubscribedCallback(self, callback: object) -> bool:
        """Set callback for item subscribed

        :param callback: callable
        :return: bool
        """
        self._RemoteStorageSubscribePublishedFileResult = self._RemoteStorageSubscribePublishedFileResult_t(callback)
        self.steam._cdll.Workshop_SetItemSubscribedCallback(self._RemoteStorageSubscribePublishedFileResult)
        return True


    def SetItemUnubscribedCallback(self, callback: object) -> bool:
        """Set callback for item unsubscribed

        :param callback: callable
        :return: bool
        """
        self._RemoteStorageUnubscribePublishedFileResult = self._RemoteStorageUnubscribePublishedFileResult_t(callback)
        self.steam._cdll.Workshop_SetItemUnubscribedCallback(self._RemoteStorageUnubscribePublishedFileResult)
        return True


    def CreateItem(self, app_id: int, filetype: EWorkshopFileType, callback: object = None, override_callback: bool = False) -> None:
        """Creates a new workshop item with no content attached yet

        :param app_id: int
        :param filetype: EWorkshopFileType
        :param callback: callable
        :param override_callback: bool
        :return: None
        """
        if callback:
            if self._CreateItemResult and override_callback:
                self.SetItemCreatedCallback(callback)

        else:
            self.SetItemCreatedCallback(callback)

        self.steam.Workshop_CreateItem(app_id, filetype)


    def SubscribeItem(self, published_file_id: int, callback: object = None, override_callback: bool = False) -> None:
        """ Subscribe to a UGC (Workshp) item

        :param published_file_id: int
        :param callback: callable
        :param override_callback: bool
        :return:
        """
        if callback:
            if self._RemoteStorageSubscribePublishedFileResult and override_callback:
                self.SetItemSubscribedCallback(callback)

        else:
            self.SetItemSubscribedCallback(callback)

        self.steam.Workshop_SubscribeItem(published_file_id)


    def UnsubscribeItem(self, published_file_id: int, callback: object = None, override_callback: bool = False) -> None:
        """ Unubscribe to a UGC (Workshp) item

        :param published_file_id: int
        :param callback: callable
        :param override_callback: bool
        :return:
        """
        if callback:
            if self._RemoteStorageUnsubscribePublishedFileResult and override_callback:
                self.SetItemUnsubscribedCallback(callback)

        else:
            self.SetItemUnsubscribedCallback(callback)

        self.steam.Workshop_UnubscribeItem(published_file_id)


    def StartItemUpdate(self, app_id: int, published_file_id: int) -> int:
        """ Start the item update process and receive an update handle

        :param app_id: int
        :param published_file_id: int
        :return: int
        """
        return self.steam.Workshop_StartItemUpdate(app_id, c_uint64(published_file_id))


    def SetItemTitle(self, update_handle: int, title: str) -> bool:
        """Set the title of a Workshop item

        :param update_handle: int
        :param title: str
        :return: bool
        """
        if len(title) > 128:
            raise AttributeError('title exceeds 128 characters')

        return self.steam.Workshop_SetItemTitle(update_handle, title.encode())


    def SetItemDescription(self, update_handle: int, description: str) -> bool:
        """Set the description of a Workshop item

        :param update_handle: int
        :param description: str
        :return: bool
        """
        if len(description) > 8000:
            raise AttributeError('description exceeds 8000 characters')

        return self.steam.Workshop_SetItemDescription(update_handle, description.encode())


    def SetItemContent(self, update_handle: int, content_directory: str) -> bool:
        """ Set the directory containing the content you wish to upload to Workshop

        :param update_handle: int
        :param content_directory: str
        :return: bool
        """
        return self.steam.Workshop_SetItemContent(update_handle, content_directory.encode())


    def SetItemPreview(self, update_handle: int, preview_image: str) -> bool:
        """Set the preview image of the Workshop item.

        :param update_handle: int
        :param preview_image: str (absolute path to a file on disk)
        :return: bool
        """
        return self.steam.Workshop_SetItemPreview(update_handle, preview_image.encode())


    def SubmitItemUpdate(self, update_handle: int, change_note: int, callback: object = None, \
                         override_callback: bool = False) -> None:
        """Submit the item update with the given handle to Steam

        :param update_handle: int
        :param change_note: str
        :param callback: callable
        :param override_callback: bool
        :return: None
        """
        if callback:
            if self._SubmitItemUpdateResult and override_callback:
                self.SetItemUpdatedCallback(callback)

        else:
            self.SetItemUpdatedCallback(callback)

        self.steam.Workshop_SubmitItemUpdate(update_handle, change_note.encode())


    def GetItemUpdateProgress(self, update_handle: int) -> dict:
        """Get the progress of an item update request

        :param update_handle: int
        :return: dict
        """
        punBytesProcessed = pointer(c_uint64)
        punBytesTotal = pointer(c_uint64)

        update_status = self.steam.Workshop_GetItemUpdateProgress(update_handle, punBytesProcessed, punBytesTotal)

        return {
            'status' : EItemUpdateStatus(update_status),
            'processed' : punBytesProcessed.contents.value,
            'total' : punBytesTotal.contents.value,
            'progress' : ( punBytesProcessed.contents.value / punBytesTotal.contents.value )
        }


    def GetNumSubscribedItems(self) -> int:
        """Get the total number of items the user is subscribed to for this game or application

        :return: int
        """
        return self.steam.Workshop_GetNumSubscribedItems()


    def SuspendDownloads(self, paused: bool = True) -> None:
        """Suspend active workshop downloads

        :param paused: bool
        :return: None
        """
        return self.steam.Workshop_SuspendDownloads(paused)


    def GetSubscribedItems(self, max_items: int = 0) -> list:
        """Get a list of published file IDs that the user is subscribed to

        :param max_items: int
        :return:
        """
        if max_items <= 0:
            max_items = SteamWorkshop.GetNumSubscribedItems()

        if max_items == 0:
            return []

        published_files_ctype = c_uint64 * maxEntries
        published_files = published_files_ctype()

        # TODO: We might need to add an exception check here to catch any errors while
        # writing to the 'pvecPublishedFileIds' array.
        actual_item_count = Steam.cdll.Workshop_GetSubscribedItems(published_files, max_items)
        # According to sdk's example, it is possible for numItems to be greater than maxEntries so we crop.
        if actual_item_count > max_items:
            published_files = published_files[:max_items]

        return published_files


    def GetItemState(self, published_file_id: int) -> EItemState:
        """Get the current state of a workshop item

        :param published_file_id: published_file_id
        :return: EItemState
        """
        return EItemState(self.steam.Workshop_GetItemState(published_file_id))


    def GetItemInstallInfo(self, published_file_id: int, max_path_length: int = 1024) -> dict:
        """Get info about an installed item

        :param published_file_id: int
        :param max_path_length: str
        :return: dict
        """
        punSizeOnDisk = pointer(c_uint64(0))
        punTimeStamp = pointer(c_uint32(0))
        pchFolder = create_string_buffer(max_path_length)

        is_installed = self.steam.Workshop_GetItemInstallInfo(
            published_file_id, punSizeOnDisk, pchFolder, max_path_length, punTimeStamp)

        if not is_installed:
            return {}

        return {
            'disk_size' : pchFolder.contents.value,
            'folder' : pchFolder.value.decode(),
            'timestamp' : punTimeStamp.contents.value
        }


    def GetItemDownloadInfo(self, published_file_id: int) -> dict:
        """Get download info for a subscribed item

        :param published_file_id: int
        :return:
        """
        punBytesDownloaded = pointer(c_uint64(0))
        punBytesTotal = pointer(c_uint64(0))

        # pBytesTotal will only be valid after the download has started.
        available = self.steam.Workshop_GetItemDownloadInfo(published_file_id, punBytesDownloaded, punBytesTotal)
        if available:
            downloaded = punBytesDownloaded.contents.value
            total = punBytesTotal.contents.value

            return {
                'downloaded' : downloaded,
                'total' : total,
                'progress' : 0.0 if total <= 0 else ( downloaded / total )
            }

        return {}
