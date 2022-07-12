import requests
import json

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

expected_response = {
        'statusCode': 200
    }

event = {
    'foo':'bar'
}

print('Triggering getting-tweets lambda function...')
actual_response = requests.post(url, json=event).json()

print(json.dumps(actual_response, indent=2))

assert expected_response == actual_response, 'Received unexpected response.'
print('Getting Tweets Lambda function status: OK.')