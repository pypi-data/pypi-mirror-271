from azure.storage.blob import ContainerClient

from .utils import list_container_directory_files

class DatalakeDirectory:
    # pass this class as source to target class
    def __init__(self, sas_url, source_directory_name):
        # authenticate
        self.source_container_client = ContainerClient.from_container_url(container_url=sas_url)

        self.source_directory_name = source_directory_name
        self.source_directory_file_paths = list_container_directory_files(self.source_container_client, self.source_directory_name)
        self.source_directory_file_names = [x.replace(self.source_directory_name,"") for x in self.source_directory_file_paths]
    
    def upload_file(self, source_file_path, target_container_client, target_file_path):
        source_blob_client = self.source_container_client.get_blob_client(source_file_path)
        target_blob_client = target_container_client.get_blob_client(target_file_path)
        
        target_blob_client.upload_blob(source_blob_client.url)