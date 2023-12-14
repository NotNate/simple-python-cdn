import os

class CacheManager:
    '''
    A class to manage the caching of content on the file system.
    It allows caching and retrieval of content based on filenames.

    :param dir: The directory where the cached content will be stored.
    '''
    def __init__(self, dir):
        '''
        Initializes the CacheManager instance.

        :param dir: The directory where the cache will be stored.
        Creates the directory if it doesn't already exist.
        '''
        self.cache_directory = dir
        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)
            
    def cache_content(self, content, filename):
        '''
        Caches the given content under the specified filename.

        :param content: The binary content to be cached.
        :param filename: The name of the file under which the content will be stored.
        Writes the content to a file in the cache directory.
        '''
        file_path = os.path.join(self.cache_directory, filename)
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Content cached at: {file_path}")
    
    def retrieve_content(self, filename):
        '''
        Retrieves the content of a cached file, if it exists.

        :param filename: The name of the file to be retrieved.
        :return: The content of the file if it exists, otherwise None.
        Reads the file's content and returns it.
        '''
        file_path = os.path.join(self.cache_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        return None
