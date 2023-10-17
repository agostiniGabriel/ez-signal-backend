from flask import request, jsonify, make_response
from flask_restful import Resource
from utils.azure_utils import Azure_Utils

class File_Helper(Resource):
    def get(self,file_id):
        conn = Azure_Utils()
        conn.connect()
        response = make_response()
        response.data = conn.read_file(file_id).readall()
        return response