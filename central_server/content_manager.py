import os
from werkzeug.utils import secure_filename
import sqlite3

class ContentManager:
    '''
    A class to manage content storage, retrieval, and tracking of downloads.
    Handles file operations and interactions with a database for download tracking.
    '''
    def __init__(self, db_path='files.db'):
        '''
        Initialize the ContentManager with a specific database path.
        
        Parameters:
        db_path (str): Path to the SQLite database file.
        '''
        self.content_directory = 'static/'
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    filename TEXT PRIMARY KEY,
                    downloads INTEGER DEFAULT 0
                );            
            ''')
    
    def increment_download(self, filename):
        '''
        Update the popularity of a file in the databse.

        Parameters:
        filename (str): The name of the file to be updated.

        Returns:
        None.
        '''
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''         
                INSERT INTO files (filename, downloads)
                VALUES (?, 1)
                ON CONFLICT(filename) DO UPDATE SET downloads = downloads + 1;
                         ''',(filename,))
    
    def get_popular_content(self, limit=5):
        '''
        Retrieve content from the content directory.

        Parameters:
        limit (int): Amount of files to retrieve.

        Returns:
        Content: The list of the limit most popular files.
        '''
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT filename FROM files
                ORDER BY downloads DESC
                LIMIT ?;''', (limit,))
            all_files = cursor.fetchall()
        
        return [file[0] for file in all_files if os.path.exists(os.path.join(self.content_directory, file[0]))]
            
    def retrieve_content(self, filename):
        '''
        Retrieve content from the content directory.

        Parameters:
        filename (str): The name of the file to be retrieved.

        Returns:
        Content: The content of the file or None if not found.
        '''
        file_path = os.path.join(self.content_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        return None

    def upload_content(self, file):
        '''
        Handle uploading and saving of content.
        Saves the file to the content directory and performs any additional processing.

        Parameters:
        file (FileStorage): The file object to be uploaded.
        '''
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.content_directory, filename)
            file.save(file_path)
            print(f"File uploaded: {file_path}")

    def delete_content(self, filename):
        '''
        Delete a specific file from the content directory.
        Checks if the file exists and then deletes it. If the file is not found,
        it raises a FileNotFoundError.

        Parameters:
        filename (str): The name of the file to be deleted.
        '''
        file_path = os.path.join(self.content_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            raise FileNotFoundError(f"File {filename} not found")

    def list_content(self):
        '''
        List all files in the content directory.
        Returns a list of filenames present in the content directory.

        Returns:
        list: A list of filenames in the content directory.
        '''
        content_files = os.listdir(self.content_directory)
        return content_files
