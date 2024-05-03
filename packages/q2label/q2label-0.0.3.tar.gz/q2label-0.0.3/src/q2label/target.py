from datetime import datetime

from azure.storage.blob import ContainerClient

from .utils import list_container_files

class TargetDirectory:
    def __init__(self, sas_url, target_directory_name, source_object):        
        self.target_container_client = ContainerClient.from_container_url(container_url=sas_url)
        self.target_directory_name = target_directory_name if target_directory_name[-1] == "/" else target_directory_name + "/"
        
        self.target_container_files = list_container_files(self.target_container_client)

        # source storage object, either datalake directory or local directory
        self.source_object = source_object

    def upload_dir(self):
        start_upload_time = datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
        for source_file_path in self.source_object.source_directory_file_paths: 
            file_name = source_file_path.replace(self.source_object.source_directory_name,"").replace("/","")
            target_file_path = self.target_directory_name + start_upload_time + "/" + file_name
            
            if file_name in self.target_container_files:
                print(f"{file_name} already uploaded at target container!")
            else:
                self.source_object.upload_file(source_file_path,
                                               self.target_container_client, 
                                               target_file_path) 
                print(f"Copied {file_name}!")
