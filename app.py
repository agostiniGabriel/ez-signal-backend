from flask import Flask
from flask_restx import Api
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

if __name__ == '__main__':
    print('Inicializando App')
    app.run(debug=True)