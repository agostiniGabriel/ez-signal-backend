import matplotlib.pyplot as plt
import numpy as np
import librosa
import json
import io
from utils.azure_utils import Azure_Utils
from utils.meta_utils import loadMetadata
from utils.request_handler_utils import validateRequestParams
from utils.response_utils import success_response, server_error_response
from flask_restx import Resource
from flask import request
from scipy.fftpack import fft



metadata = loadMetadata('./resources/resourceMeta/audio_frequency_plot-meta.json')
template_post_body = metadata['requestBody']

class Audio_Frequency_Plot(Resource):
    def post(self):
        success, params, response = validateRequestParams(template_post_body, request)
        if not success:
            return response
        az = Azure_Utils()
        audio = az.read_file(params.get('fileId'))
        signal, sample_rate = librosa.load(audio)
        signal = signal[:sample_rate]
        frequency_domain_signal = fft(signal)
        plt.switch_backend('Agg') 
        plt.xlabel(params.get('xLabel'))
        plt.ylabel(params.get('yLabel'))
        plt.title(params.get('title'))
        plt.plot(np.abs(frequency_domain_signal[:sample_rate//2]),lw=params.get('lineWidth',0.3))
        stream = io.BytesIO()
        plt.savefig(stream, format='png', bbox_inches='tight')
        stream.seek(0)
        try:
            result_file_id = az.upload_stream(stream, '.png')
            return success_response(content_type = 'application/json', body = json.dumps({'fileId':result_file_id, 'fileType':'png'}))
        except Exception as excpt:
            error = 'An exception happened during result upload to storage: ' + str(excpt)
            return server_error_response(body = error) 