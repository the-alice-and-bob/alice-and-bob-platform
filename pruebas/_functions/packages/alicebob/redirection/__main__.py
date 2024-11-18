import time

import requests

URL = "https://faas-ams3-2a2df116.doserverless.co/api/v1/web/fn-d3c5b8e2-cbcd-4c8d-833d-8bb36e317589/alicebob/inoreader?blocking=false&result=false"
AUTH_TOKEN = "uef7b36135154447faf16d6a8ff19b0c12605d0eae16144399165aa1edf7e1c5d"
DO_SERVERLESS_AUTH = "Fh7CVSeRooVuQym"


def main(event, context):

    request_data = {
        "body": event,
        "headers": {
            "Content-Type": "application/json"
        },
        "token": AUTH_TOKEN,
        "method": "POST",
    }

    print(f"[*] Request: {request_data} ({time.time()})", flush=True)
    response = requests.post(URL, json=request_data, headers={
        "Content-Type": "application/json",
        "X-Require-Whisk-Auth": DO_SERVERLESS_AUTH
    })

    print(f"[!] Response: {response.text} ({time.time()})", flush=True)

    return {
        "statusCode": response.status_code,
        "body": response.text
    }
