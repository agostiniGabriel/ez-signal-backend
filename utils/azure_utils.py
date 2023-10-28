from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import uuid
import os
import io

class Azure_Utils:
    def __init__(self):
        self.azure_credential = DefaultAzureCredential()
        self.account_url = os.environ.get('ACCOUNT_URL')
        self.container = os.environ.get('CONTAINER')
        self.connect()
        
    def connect(self):
        self.blob_service_client = BlobServiceClient(self.account_url, credential=self.azure_credential)
    
    def upload_file(self,local_path):
        _filename, file_extension = os.path.splitext(local_path)
        with open(file=local_path, mode="rb") as data:
            unique_file_name = self.upload_stream(data,file_extension)
        return unique_file_name
    
    def upload_stream(self, byte_stream, file_extension):
        unique_file_name = f'{self.generate_unique_id()}{file_extension}'
        blob_client = self.blob_service_client.get_blob_client(container = self.container, blob = unique_file_name)
        blob_client.upload_blob(byte_stream)
        return unique_file_name
    
    def read_file(self,unique_file_name):
        blob = self.blob_service_client.get_blob_client(container = self.container, blob = unique_file_name)
        stream = io.BytesIO() 
        blob.download_blob().readinto(stream)
        stream.seek(0)
        return stream

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()) 


