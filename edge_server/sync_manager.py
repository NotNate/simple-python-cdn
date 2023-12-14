import requests
import os
import threading

class SyncManager:
    '''
    A class to manage synchronization of content from a central server to the local cache.

    :param center_server_url: URL of the central server from which to sync content.
    :param cm: An instance of CacheManager for managing local cache.
    :param sync_interval: Time interval (in seconds) for synchronization operations.
    '''
    def __init__(self, center_server_url, cm, sync_interval):
        '''
        Initializes the SyncManager instance.

        :param center_server_url: URL of the central server for syncing.
        :param cm: Instance of CacheManager for managing the cache.
        :param sync_interval: Interval in seconds for periodic sync operations.
        '''
        self.central_server_url = center_server_url
        self.cache_manager = cm
        self.sync_int = sync_interval
    
    def synchronize(self):
        '''
        Synchronizes the most popular content from the central server to the local cache.
        It fetches a list of popular content, compares it with the local cache,
        and downloads any missing content.

        This method is scheduled to run periodically based on the sync_interval.
        '''
        print("Starting synchronize")
        response = requests.get(f"{self.central_server_url}/popular/5")
        if response.status_code == 200:
            content_list = response.json()['content']
            my_list = os.listdir(self.cache_manager.cache_directory)
            for content in content_list:
                if content not in my_list:
                    file_url = f"{self.central_server_url}/fetch/{content}"
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        self.cache_manager.cache_content(file_response.content, content)
            print("Finished sync")
        threading.Timer(self.sync_int, self.synchronize).start()