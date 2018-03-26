import random
import json
import requests

# API requirments for Rightscale
# Get access_token for all the queries to be performed
def get_accesstoken():
    launch_url = "https://us-4.rightscale.com/api/oauth2"
    header = {'X-API-Version': '1.5'}
    got_response = requests.post(launch_url, headers=header, data={'grant_type': 'refresh_token', 'refresh_token': token_refresh})
    json_data = json.loads(got_response.text)
    access_token = json_data["access_token"]
    return access_token

# This is the main function that alexa would look at
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    if event['request']['type'] == "IntentRequest":
        sessionAttributes: {
            numberOfRequests: 1
            }
        return intent_router(event, context)

# This is launch response for Alexa
def on_launch(event, context):
    response = {
        'version' : '1.0',
        'response':{
            'outputSpeech':{
                'type': 'PlainText',
                'text': 'welcome to rightscale, Nani' ,
            }
        }
    }
    return response

# Intent router depending on type of intent
def intent_router(event, context):
    intent = event['request']['intent']['name']
    if intent == "getserverlist":
        return instance_metrics(event, context)
    if intent == "deployserver":
        return launch_server(event, context)
    if intent == "teminateserver":
        return terminate_server(event, context)

# Definition to get server count
def instance_metrics(event, context):
    access_token = get_accesstoken()
    bearer_token = 'Bearer ' + access_token
    header = {'X-API-Version': '1.0', 'Authorization': bearer_token}
    url = "https://analytics.rightscale.com/api/instance_metrics/actions/current_count"
    got_response = requests.get(url, headers=header)
    json_data = json.loads(got_response.text)
    number_count = json_data['current_instances_count']
    response = {
        'version' : '1.0',
        'response':{
            'outputSpeech':{
                'type': 'PlainText',
                'text':  number_count ,
            }
        }
    }
    return response

# Definition for launching server
def launch_server(event, context):
    access_token = get_accesstoken()
    bearer_token = 'Bearer ' + access_token
    header = {'X-API-Version': '1.5', 'Authorization': bearer_token}
    launch_url = "https://us-4.rightscale.com/api/servers/<server_id>/launch.xml"
    got_response = requests.post(launch_url, headers=header)
    response = {
        'version' : '1.0',
        'response':{
            'outputSpeech':{
                'type': 'PlainText',
                'text':  'Server launched' ,
            }
        }
    }
    return response

# Definition for terminating server
def terminate_server(event, context):
    access_token = get_accesstoken()
    bearer_token = 'Bearer ' + access_token
    header = {'X-API-Version': '1.5', 'Authorization': bearer_token}
    terminate_url = "https://us-4.rightscale.com/api/servers/<server_id>/terminate"
    got_response = requests.post(terminate_url, headers=header)
    response = {
        'version' : '1.0',
        'response':{
            'outputSpeech':{
                'type': 'PlainText',
                'text':  'Server terminated!' ,
            }
        }
    }
    return response
