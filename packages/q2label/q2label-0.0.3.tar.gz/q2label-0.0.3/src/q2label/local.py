import os

class LocalDirectory:
    # pass this class as source to target class
    def __init__(self, directory_path):
        self.directory_path = directory_path 
        self.source_directory_name = self.directory_path.split('\\')[-1]
        self.source_directory_parent = self.directory_path.replace(self.source_directory_name,"")
        self.source_directory_file_names = os.listdir(self.directory_path)
        self.source_directory_file_paths = [self.source_directory_name + '/' + x for x in self.source_directory_file_names]
    
    def upload_file(self, source_file_path, target_container_client, target_file_path):
        full_file_path = os.path.join(self.source_directory_parent , source_file_path)
        with open(full_file_path, 'rb') as data:
            target_container_client.upload_blob(name=target_file_path, data=data)