from flask import Flask
from flask_restful import Api, Resource
from resources.file_helper import File_Helper
from resources.audio_time_plot import Audio_Time_Plot
from resources.audio_spectogram_plot import Audio_Spectogram_Plot
from resources.server_status import Server_Status

app = Flask(__name__)
api = Api(app)

api.add_resource(File_Helper, '/retrievefile/<file_id>') 
api.add_resource(Audio_Time_Plot, '/plotAudio/timeDomain')
api.add_resource(Audio_Spectogram_Plot, '/plotAudio/spectogram')
api.add_resource(Server_Status, '/status')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

class Customers(Resource):
    def get(self):      
        return "Test", 200
    
# Create API routes
api.add_resource(Customers, '/customers')

# if __name__ == '__main__':
#     print('Inicializando App')
#     app.run(debug=True)