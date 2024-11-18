import json

import requests


URL = "https://faas-ams3-2a2df116.doserverless.co/api/v1/web/fn-d3c5b8e2-cbcd-4c8d-833d-8bb36e317589/alicebob/inoreader"


def main():

    with open("functions/packages/alicebob/inoreader/inoreader-01.json", "r") as file:
        json_data = json.load(file)

    json_data["token"] = "uef7b36135154447faf16d6a8ff19b0c12605d0eae16144399165aa1edf7e1c5d"

    query_params = {
        "blocking": "false",
        "result": "false"
    }

    query_params_string = "&".join([f"{key}={value}" for key, value in query_params.items()])

    query_url = f"{URL}?{query_params_string}"
    print(query_url)

    response = requests.post(query_url, json=json_data, headers={
        "Content-Type": "application/json",
        # "X-Require-Whisk-Auth": "Fh7CVSeRooVuQym"
        "X-Require-Whisk-Auth": "Fh7CVSeRooVuQym"
    })

    print(response.text)


if __name__ == '__main__':
    main()
