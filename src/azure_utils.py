from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import uuid
import os

class Azure_Utils:
    def __init__(self, account_url, container = 'dev'):
        self.azure_credential = DefaultAzureCredential()
        self.account_url = account_url
        self.container = container
        
    def connect(self):
        self.blob_service_client = BlobServiceClient(self.account_url, credential=self.azure_credential)
    
    def upload_file(self,local_path):
        _filename, file_extension = os.path.splitext(local_path)
        unique_file_name = f'{self.generate_unique_id()}.{file_extension}'
        blob_client = self.blob_service_client.get_blob_client(container = self.container, blob = unique_file_name)
        with open(file=local_path, mode="rb") as data:
            blob_client.upload_blob(data)

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()) 


