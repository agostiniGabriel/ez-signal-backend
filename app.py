from flask import Flask
from flask_restful import Api
from resources.file_helper import File_Helper
from resources.audio_time_plot import Audio_Time_Plot
from resources.audio_spectogram_plot import Audio_Spectogram_Plot

from json import dumps

app = Flask(__name__)
api = Api(app)

api.add_resource(File_Helper, '/retrievefile/<file_id>') 
api.add_resource(Audio_Time_Plot, '/plotAudio/timeDomain')
api.add_resource(Audio_Spectogram_Plot, '/plotAudio/spectogram')

if __name__ == '__main__':
    app.run(port=5000,debug=True)