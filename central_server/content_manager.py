import os
from werkzeug.utils import secure_filename

class ContentManager:
    def __init__(self):
        """
        Initialize the ContentManager.
        Sets up the directory where content will be stored and managed.
        """
        self.content_directory = 'static/'
        
    def retrieve_content(self, filename):
        file_path = os.path.join(self.content_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        return None

    def upload_content(self, file):
        """
        Handle uploading and saving of content.
        Saves the file to the content directory and performs any additional processing.

        Parameters:
        file (FileStorage): The file object to be uploaded.
        """
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.content_directory, filename)
            file.save(file_path)
            print(f"File uploaded: {file_path}")

    def delete_content(self, filename):
        """
        Delete a specific file from the content directory.
        Checks if the file exists and then deletes it. If the file is not found,
        it raises a FileNotFoundError.

        Parameters:
        filename (str): The name of the file to be deleted.
        """
        file_path = os.path.join(self.content_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            raise FileNotFoundError(f"File {filename} not found")

    def list_content(self):
        """
        List all files in the content directory.
        Returns a list of filenames present in the content directory.

        Returns:
        list: A list of filenames in the content directory.
        """
        content_files = os.listdir(self.content_directory)
        return content_files
