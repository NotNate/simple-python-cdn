import os

class CacheManager:
    def __init__(self, dir):
        self.cache_directory = dir
        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)
            
    def cache_content(self, content, filename):
        file_path = os.path.join(self.cache_directory, filename)
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Content cached at: {file_path}")
    
    def retrieve_content(self, filename):
        file_path = os.path.join(self.cache_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        return None
