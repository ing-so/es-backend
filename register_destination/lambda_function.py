# epson에서 제공받은 복합기

import sys
import uuid
from urllib import request, parse, error
from http import HTTPStatus
import base64
import json

HOST = 'api.epsonconnect.com'       # You will receive it when the license is issued.
ACCEPT = 'application/json;charset=utf-8'

def lambda_handler(event, context):
    print("Event received:", event)
    print("Event type:", type(event))

    # Ensure the event contains 'name'
    if 'body' not in event:
        raise ValueError("Missing 'body' in event data")

    body = event['body']
    print("body: ", body)
    print("body_type: ", type(body))
    body_dict = json.loads(body)
    print(type(body_dict))
    
    name = body_dict['name']
    print("name: ", name)
    print("name: ", type(name))

    # 1. Authentication
    AUTH_URI = 'https://' + HOST + '/api/1/printing/oauth2/auth/token?subject=printer'
    CLIENT_ID = '####################'
    SECRET = '##############################'
    DEVICE = '##############################'

    auth = base64.b64encode((CLIENT_ID + ':' + SECRET).encode()).decode()

    query_param = {
        'grant_type': 'password',
        'username': DEVICE,
        'password': ''
    }
    query_string = parse.urlencode(query_param)

    headers = {
        'Authorization': 'Basic ' + auth,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }

    req, res, body, err_str = '', '', '', ''
    try:
        req = request.Request(AUTH_URI, data=query_string.encode('utf-8'), headers=headers, method='POST')
        with request.urlopen(req) as res:
            body = res.read()
    except error.HTTPError as err:
        err_str = str(err.code) + ':' + err.reason + ':' + str(err.read())
    except error.URLError as err:
        err_str = err.reason

    print('\n 1. Authentication: ---------------------------------')
    if res == '':
        print(err_str)
        raise Exception(f"Authentication failed: {err_str}")
    else:
        print(str(res.status) + ':' + res.reason)
        print(json.loads(body))

    if err_str != '' or res.status != HTTPStatus.OK:
        raise Exception(f"Authentication failed with status {res.status}")

    # 2. Register scan destination
    subject_id = json.loads(body).get('subject_id')
    access_token = json.loads(body).get('access_token')

    add_uri = 'https://' + HOST + '/api/1/scanning/scanners/' + subject_id + '/destinations'

    # unique alias_name = event.name + a shortened UUID
    unique_suffix = uuid.uuid4().hex[:8]
    combined_length = len(name) + len(unique_suffix) + 1
    if combined_length > 32:
        raise ValueError("event.name is too long to be combined with a unique identifier within 32 characters")
    unique_alias_name = f"{name}_{unique_suffix}"

    data_param = {
        'alias_name': unique_alias_name,  # alias_name은 중복될 수 없음
        'type': 'mail',
        'destination': '#####@#######'
    }
    data = json.dumps(data_param)

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    req, res, body, err_str = '', '', '', ''
    try:
        req = request.Request(add_uri, data=data.encode('utf-8'), headers=headers, method='POST')
        with request.urlopen(req) as res:
            body = res.read()
    except error.HTTPError as err:
        err_str = str(err.code) + ':' + err.reason + ':' + str(err.read())
    except error.URLError as err:
        err_str = err.reason

    print('\n 2. Register scan destination: ----------------------')
    print(add_uri)
    print(data)
    if res == '':
        print(err_str)
        raise Exception(f"Register scan destination failed: {err_str}")
    else:
        print(str(res.status) + ':' + res.reason)
        print(json.loads(body))

    return {
        'statusCode': 200,
        'body': json.loads(body)
    }
