def list_container_directory_files(container_client, directory_name):
    ## to move to azure specific utils --> deprecated
    directory_name = directory_name if directory_name[-1] == "/" else directory_name + "/"
    directory_blob_files = container_client.list_blobs(name_starts_with = directory_name)
    return [x.name for x in directory_blob_files]

def list_container_files(container_client):
    ''' List all files in container: excluding relative path!'''
    directory_blob_files = container_client.list_blobs()
    return [x.name.split('/')[-1]  for x in directory_blob_files]

def create_env(datalake_upload, connection_string_sink, connection_string_source = '',):
    with open(".env", "w") as env_file:
        env_file.write(f"TARGET_AZURE_CONNECTION_STRING = '{connection_string_sink}' \n")
        if datalake_upload:
            env_file.write(f"SOURCE_AZURE_CONNECTION_STRING = '{connection_string_source}' \n")