from flask import Flask
from flask_restful import Api
from resources.file_helper import File_Helper

from json import dumps

app = Flask(__name__)
api = Api(app)

api.add_resource(File_Helper, '/retrievefile/<file_id>') 

if __name__ == '__main__':
    app.run()