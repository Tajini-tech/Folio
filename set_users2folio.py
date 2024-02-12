import json
import os
from glob import glob
from urllib.parse import urljoin
import requests as r
import fake_users
import folio_auth
from datetime import datetime
url = "https://folio-snapshot-okapi.dev.folio.org/authn/login"

# prepare the json fake users

folder_name = "json_fake_users"
os.makedirs(folder_name, exist_ok=True)
fake_users = fake_users.generate_fake_user(5)
for i, user in enumerate(fake_users):
    filename = os.path.join(folder_name, "User{}.json".format(i + 1))
    with open(filename, "w", encoding='utf-8') as outfile:
        json.dump(user, outfile, indent=2, ensure_ascii=False)


# get all user ids to check after with the get request if the users are added
def get_all_user_ids():
    user_ids = list()
    for filepath in glob(os.path.join(folder_name, '*.json')):
        with open(filepath, "r", encoding="utf-8") as file:
            user_ids.append(json.load(file).get('id'))
    return user_ids


# get okapi token
token = folio_auth.get_token()


def set_users():
    for filepath in glob(os.path.join(folder_name, '*.json')):
        with open(filepath, "r", encoding="utf-8") as file:
            user_data = json.load(file)
            start_time=datetime.now()
            request = r.post(
                urljoin(url, "/users"),
                headers={"x-okapi-token": token, "Content-Type": "application/json"},
                json=user_data
            )
            if request.status_code == 201:
                print(f"time processing for 1 user is {datetime.now()-start_time}")
                print("User " + os.path.basename(filepath) + " is added successfully")
            else:
                print("cant add user" + os.path.basename(filepath) + "request Status :", request.status_code,
                      request.text)


def get_user(user_id):
    response = r.get(urljoin(url, f"/users/{user_id}"),
                     headers={"x-okapi-token": token, "Content-Type": "application/json"})
    if response.status_code == 200:
        print(response.json())
    else:
        print("cant find user" + user_id, response.status_code, response.text)
        return None


# write the users to folio
start_time=datetime.now()
set_users()
print(f"set_users ended in{datetime.now()-start_time}")
# Now we check if they are stored in folio
users_id_list = get_all_user_ids()
for i in range(len(users_id_list)):
    get_user(users_id_list[i])
