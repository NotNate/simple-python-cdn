import requests
from cache_manager import CacheManager

class SyncManager:
    def __init__(self, center_server_url, cm):
        self.central_server_url = center_server_url
        self.cache_manager = cm
    
    def synchronize(self):
        response = requests.get(f"{self.central_server_url}/list")
        if response.status_code == 200:
            content_list = response.json()['content']
            for content in content_list:
                file_url = f"{self.central_server_url}/content/{content}"
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    self.cache_manager.cache_content(file_response.content, content)