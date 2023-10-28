from flask import make_response

def bad_request_reponse(body = 'Validate your request', content_type = 'text/plain' ,custom_status = 'Bad Request'):
    return generic_response(400, custom_status, body, content_type)

def created_response(body = 'Created', content_type = 'text/plain', custom_status = 'Created'):
    return generic_response(201, custom_status, body, content_type)

def success_response(body = 'Success', content_type = 'text/plain', custom_status = 'Success'):
    return generic_response(200, custom_status, body, content_type)

def server_error_response(body = 'Error', content_type = 'text/plain', custom_status = 'Internal Server Error'):
    return generic_response(500, custom_status, body, content_type)

def generic_response(status_code, status, data, content_type):
    response = make_response()
    response.status_code = status_code
    response.status = status
    response.data = data
    response.headers.add_header('Content-Type', content_type)
    return response