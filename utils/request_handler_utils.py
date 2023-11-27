from utils.response_utils import bad_request_reponse

def validateRequestParams(template_post_body, request):
    requestPayload = request.json
    response = None
    invalidRequest, missingParam, mergedBody = findDiff(template_post_body,requestPayload,requestPayload)
    if invalidRequest:
        response = bad_request_reponse(body=f'Check the request body. Missing required parameter: {missingParam}')
    return not invalidRequest, mergedBody, response

def findDiff(d1, d2, merged_body = {}):
    for k in d1:
        if k not in d2:
            if d1[k]["isRequired"]:
                return True, k, None
            else:
                newBody = merged_body
                newBody[k] = d1[k]["defaultValue"]
                return False, None, newBody        