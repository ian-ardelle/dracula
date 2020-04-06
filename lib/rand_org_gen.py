import requests
import json
import config


def gen(pool: int, max: int, rep: bool = True) -> list:
    """

    :param pool: Number of random integers to generate
    :param max: Highest value generated from JSON request
    :type rep: Allows for replacement (true = repetition will occur)
    """
    url = "https://api.random.org/json-rpc/2/invoke"
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "generateIntegers",
        "params": {
            "apiKey": config.RANDOM_ORG_API_KEY,
            "n": pool,
            "min": 1,
            "max": max,
            "replacement": rep
        },
        "jsonrpc": "2.0",
        "id": 42,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"]
    return response["result"]["random"]["data"]
