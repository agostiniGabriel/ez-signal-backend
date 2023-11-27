from scipy.signal import butter, lfilter
import soundfile as sf
import io
import json
import librosa
from utils.azure_utils import Azure_Utils
from utils.meta_utils import loadMetadata
from utils.request_handler_utils import validateRequestParams
from utils.response_utils import success_response, server_error_response
from flask_restx import Resource
from flask import request

metadata = loadMetadata('./resources/resourceMeta/bandpass_filter-meta.json')
template_post_body = metadata['requestBody']


def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

class Bandpass_Filter(Resource):
    def post(self):
        try:
            success, params, response = validateRequestParams(template_post_body, request)
            if not success:
                return response
            az = Azure_Utils()
            order = params.get('order')
            lowcut = params.get('cutoffLowFrequency')
            highcut = params.get('cutoffHighFrequency')
            data, fs = librosa.load(az.read_file(params.get('fileId')))
            y = butter_bandpass_filter(data, lowcut, highcut, fs, order)
            stream = io.BytesIO()
            stream.name = 'file.wav'
            sf.write(stream, y, fs)
            stream.seek(0)
            result_file_id = az.upload_stream(stream, '.wav')
            return success_response(content_type = 'application/json', body = json.dumps({'fileId':result_file_id, 'fileType':'wav'}))
        except Exception as excpt:
            error = 'An exception happened: ' + str(excpt)
            return server_error_response(body = error) 
        


