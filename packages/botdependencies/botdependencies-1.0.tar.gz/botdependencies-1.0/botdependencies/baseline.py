from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core import exceptions
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient, FileSystemClient
from io import BytesIO
import io
import json
import chardet

my_conn_string = "DefaultEndpointsProtocol=https;AccountName=lzdatalakesandbox2;AccountKey=e64Y9+CWm9OanXk4AQJAs0vLeifIBYLFXGVKG5mzmv4ebZLxjvOFrxlq8sX4A1rFq2tGI+cgLWkv+AStwzOvZA==;EndpointSuffix=core.windows.net"
file_system_name = "dataanalytics"

### Set up ADLS Locations
datalake_blob_service_client = BlobServiceClient.from_connection_string(my_conn_string)
container_client = datalake_blob_service_client.get_container_client(file_system_name)

datalake_service_client = DataLakeServiceClient.from_connection_string(my_conn_string)
file_system_client = datalake_service_client.get_file_system_client(file_system_name)
directory_client = datalake_service_client.get_directory_client(file_system_client.file_system_name, "botfiles")

file_path = 'botfiles/Book8.xlsx'
file_client = file_system_client.get_file_client(file_path)
first_file = file_client.download_file()

data = first_file.readall()
df = pd.read_excel(BytesIO(data))


json_data = df.to_json()
print(json_data)

#keywords_tags_dict = df.set_index('Keywords')['Tags'].to_dict()
#keywords_tags_dict = df.to_json(orient='records', lines=True)

def get_keywords_tags_dict():
    #return keywords_tags_dict
    return json_data