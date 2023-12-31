import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import json
from utils.azure_utils import Azure_Utils
from utils.request_handler_utils import validateRequestParams
from utils.response_utils import success_response, server_error_response
from flask_restx import Resource
from flask import request
from utils.meta_utils import loadMetadata

metadata = loadMetadata('./resources/resourceMeta/audio_spectogram_plot-meta.json')
template_post_body = metadata['requestBody']

class Audio_Spectogram_Plot(Resource):
    def post(self):
        success, params, response = validateRequestParams(template_post_body, request)
        if not success:
            return response
        az = Azure_Utils()
        plt.switch_backend('Agg') 
        y, sr = librosa.load(az.read_file(params["fileId"]))
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time',sr=sr, ax=ax)
        ax.set(title=params.get('title',''))
        ax.label_outer()
        print(ax.get_xlim())
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        stream = io.BytesIO()
        plt.savefig(stream, format='png', bbox_inches='tight')
        stream.seek(0)
        try:
            result_file_id = az.upload_stream(stream, '.png')
            return success_response(content_type = 'application/json', body = json.dumps({'fileId':result_file_id, 'fileType':'png'}))
        except Exception as excpt:
            error = 'An exception happened during result upload to storage: ' + str(excpt)
            return server_error_response(body = error) 
