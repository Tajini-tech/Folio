import time
import requests as r

header = {"x-okapi-tenant": "diku"}
login = {"username": "diku_admin", "password": "admin"}
# url = "https://folio-snapshot-2-okapi.dev.folio.org/authn/login"
url = "https://folio-snapshot-okapi.dev.folio.org/authn/login"
token_info = {"token": None, "expiration_time": 0}

def get_token(url=url, header=header, login=login):
    global token_info
    # Check if the stored token is still valid
    if token_info["token"] and token_info["expiration_time"] > time.time():
        return token_info["token"]
    response = r.post(url, headers=header, json=login)
    if response.status_code == 201:
        print("Response headers", response.headers)
        token = response.headers.get("x-okapi-token")
        if token:
            expiration_header = response.headers.get("x-okapi-token-expiration", 0)
            expiration_time = time.time() + int(expiration_header)
            token_info = {"token": token, "expiration_time": expiration_time}
            print("New x-okapi-token:", token)
            print("Expiration time:", expiration_time)
            return token
        else:
            print("No token found")
    else:
        print(response.status_code, response.text)
