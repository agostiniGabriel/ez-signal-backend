from flask import Flask
from flask_restx import Api
from resources.file_helper import File_Helper
from resources.audio_time_plot import Audio_Time_Plot
from resources.audio_spectogram_plot import Audio_Spectogram_Plot
from resources.server_status import Server_Status
from resources.audio_frequency_plot import Audio_Frequency_Plot
from resources.lowpass_filter import Lowpass_Filter
from resources.bandpass_filter import Bandpass_Filter
from resources.highpass_filter import Highpass_Filter

app = Flask(__name__)
api = Api(app)

api.add_resource(File_Helper, '/retrievefile/<file_id>') 
api.add_resource(Audio_Time_Plot, '/plotAudio/timeDomain')
api.add_resource(Audio_Spectogram_Plot, '/plotAudio/spectogram')
api.add_resource(Audio_Frequency_Plot, '/plotAudio/frequencyDomain')
api.add_resource(Lowpass_Filter, '/applyFilter/lowpass')
api.add_resource(Bandpass_Filter, '/applyFilter/bandpass')
api.add_resource(Highpass_Filter, '/applyFilter/highpass')
api.add_resource(Server_Status, '/status')

if __name__ == '__main__':
    print('Inicializando App')
    app.run(debug=True)