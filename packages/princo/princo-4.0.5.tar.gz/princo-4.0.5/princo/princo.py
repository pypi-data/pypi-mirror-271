import requests


def check_credit():
    response = requests.post("http://localhost:3000/api/verifyCredit")
    if response.status_code == 200:
        return response.json()
    else:
        return None
