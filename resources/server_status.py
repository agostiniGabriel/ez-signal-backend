from flask_restful import Resource
from utils.response_utils import success_response

class Server_Status(Resource):
    def get(self):
        return success_response(body="Server Listening")