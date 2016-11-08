import requests
import simplejson as json
import time
import hmac

url = 'https://api.fitbit.com/oauth2/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic MjI3WkZMOmQyZDI3NjBmZWZiOTU0ZGVjZTZhNDI3OTk1OTRiYjYw'}


def get_token(code):
    payloads = {'redirect_uri': 'http://166.104.231.227:8080/callback', 'clientId':'227ZFL', 'grant_type':'authorization_code'}# append code
    payloads['code'] = code
    response = requests.post(url, headers=headers, data=payloads, verify=False)
    json_response = json.loads(response.text)
    print '***************'
    print response.content
    print '***************'
    if 'success' in json_response:
        return json.loads(response.text)
    access_token = json_response['access_token']
    expires_in = json_response['expires_in']
    refresh_token = json_response['refresh_token']
    scope = json_response['scope']
    token_type = json_response['token_type']
    user_id = json_response['user_id']
    json_response['success'] = True
    return json_response


def get_refresh_token(refresh_token):
    payloads = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    response = requests.post(url, headers=headers, data=payloads, verify=False)
    json_response = json.loads(response.text)
    print '***************'
    print response.content
    print '***************'
    if 'success' in json_response:
        return json.loads(response.text)
    access_token = json_response['access_token']
    expires_in = json_response['expires_in']
    refresh_token = json_response['refresh_token']
    scope = json_response['scope']
    token_type = json_response['token_type']
    user_id = json_response['user_id']
    json_response['success'] = True
    return json_response

def is_token_expired(response):
    try:
        print response['errors'][0]['message'].split(:)[0]
        if response['errors'][0]['message'].split(:)[0] == 'Access token expired':
            return True
        return False
    except Exception, e:
        return False

def make_key(user_id):
    timestamp = int(time.time())
    key = hmac.new(str(user_id)+str(timestamp)).hexdigest()
    return key
