from flask import make_response
from flask_restx import Resource
from utils.azure_utils import Azure_Utils

class File_Helper(Resource):
    def get(self,file_id):
        conn = Azure_Utils()
        response = make_response()
        stream = conn.read_file(file_id)
        stream.seek(0)
        response.data = stream.read()
        return response