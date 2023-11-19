import json

def loadMetadata(path):
    with open(path,'r') as metadata_file:
        metadata = json.load(metadata_file)
    return metadata