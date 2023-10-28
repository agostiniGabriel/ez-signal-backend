import wave
import numpy as np
import matplotlib.pyplot as plt
import io
import json
from utils.azure_utils import Azure_Utils
from utils.request_handler_utils import validateRequestParams
from utils.response_utils import bad_request_reponse, success_response, server_error_response
from flask_restful import Resource
from flask import request

fullMode = 'FULL'
intervalMode = 'INTERVAL'

template_post_body = {
    'fileId': {
        'isRequired': True
    },
    'mode':{
        'isRequired': False,
        'defaultValue': fullMode
    },
    'interval':{
        'isRequired': False,
        'defaultValue': {
            'from': 0,
            'to': 200
        }
    },
    'xLabel':{
        'isRequired': False,
        'defaultValue': 'Time [s]'
    },
    'yLabel':{
        'isRequired': False,
        'defaultValue': 'Value'
    }
}

class Audio_Time_Plot(Resource):
    def post(self):
        success, params, response = validateRequestParams(template_post_body, request)
        if not success:
            return response
        az = Azure_Utils()
        az.connect()
        audio = az.read_file(params.get('fileId'))
        signal_wave = wave.open(audio, 'rb')
        sample_rate = signal_wave.getframerate()
        signal = np.frombuffer(signal_wave.readframes(-1), dtype=np.int16)
        if params.get('mode') == fullMode:
            signal = signal[:]
        elif params.get('mode') == intervalMode:
            interval = params.get('interval')
            signal = signal[int(interval.get('from')/1000)*sample_rate:int(interval.get('to')/1000)*sample_rate]
        else:
            return bad_request_reponse(body = 'Invalid mode. Supported modes are: FULL and INTERVAL')
        time = np.linspace(0, len(signal) / sample_rate, num=len(signal))
        plt.switch_backend('Agg') 
        plt.plot(time,signal)
        plt.xlabel(params.get('xLabel'))
        plt.ylabel(params.get('yLabel'))
        stream = io.BytesIO()
        plt.savefig(stream, format='png', bbox_inches='tight')
        stream.seek(0)
        try:
            result_file_id = az.upload_stream(stream, '.png')
            return success_response(content_type = 'application/json', body = json.dumps({'fileId':result_file_id}))
        except Exception as excpt:
            error = 'An exception happened during result upload to storage: ' + str(excpt)
            return server_error_response(body = error) 
