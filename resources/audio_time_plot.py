import wave
import numpy as np
import matplotlib.pyplot as plt
import io
import json
from utils.azure_utils import Azure_Utils
from utils.meta_utils import loadMetadata
from utils.request_handler_utils import validateRequestParams
from utils.response_utils import bad_request_reponse, success_response, server_error_response
from flask_restful import Resource
from flask import request

metadata = loadMetadata('./resources/resourceMeta/audio_time_plot-meta.json')
fullMode = metadata['constDefinition']['mode']['full']
intervalMode = metadata['constDefinition']['mode']['interval']
template_post_body = metadata['requestBody']

class Audio_Time_Plot(Resource):
    def post(self):
        success, params, response = validateRequestParams(template_post_body, request)
        if not success:
            return response
        az = Azure_Utils()
        audio = az.read_file(params.get('fileId'))
        signal_wave = wave.open(audio, 'rb')
        sample_rate = signal_wave.getframerate()
        signal = np.frombuffer(signal_wave.readframes(-1), dtype=np.int16)
        plt.switch_backend('Agg') 
        time = np.linspace(0, len(signal) / sample_rate, num=len(signal))
        if params.get('mode', fullMode) == fullMode:
            signal = signal[:]
            plt.xlim(0, time[-1])
        elif params.get('mode') == intervalMode:
            interval = params.get('interval')
            plt.xlim(interval.get('from'),interval.get('to'))
        else:
            return bad_request_reponse(body = 'Invalid mode. Supported modes are: FULL and INTERVAL')
        plt.plot(time,signal, lw=params.get('lineWidth',0.3))
        plt.xlabel(params.get('xLabel'))
        plt.ylabel(params.get('yLabel'))
        plt.title(params.get('title'))
        stream = io.BytesIO()
        plt.savefig(stream, format='png', bbox_inches='tight')
        stream.seek(0)
        try:
            result_file_id = az.upload_stream(stream, '.png')
            return success_response(content_type = 'application/json', body = json.dumps({'fileId':result_file_id, 'fileType':'png'}))
        except Exception as excpt:
            error = 'An exception happened during result upload to storage: ' + str(excpt)
            return server_error_response(body = error) 
