import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from glob import glob
from urllib.parse import urljoin
import requests as r
import aDis_users
import folio_auth

url = "https://folio-snapshot-okapi.dev.folio.org/authn/login"

folder_name = "json_aDis_users"
os.makedirs(folder_name, exist_ok=True)
users = aDis_users.generate_users()
for i, user in enumerate(users):
    filename = os.path.join(folder_name, "User{}.json".format(i + 1))
    with open(filename, "w", encoding='utf-8') as outfile:
        json.dump(user, outfile, indent=2, ensure_ascii=False)

users_list = list()
for filepath in glob(os.path.join(folder_name, "*.json")):
    with open(filepath, "r",encoding="utf-8") as file:
        users_list.append(json.load(file))


# get all user ids to check after with the get request if the users are added
def get_all_user_ids():
    user_ids = list()
    for filepath in glob(os.path.join(folder_name, '*.json')):
        with open(filepath, "r", encoding="utf-8") as file:
            user_ids.append(json.load(file).get('id'))
    return user_ids


# get okapi token
token = folio_auth.get_token()


def users_batch(users_list):
    futures = list()
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for user in users_list:
            future = executor.submit(r.post, urljoin(url, "/users"),
                                     headers={"x-okapi-token": token, "Content-Type": "application/json"},
                                     json=user)
            futures.append(future)
    for future in as_completed(futures):
        response = future.result()
    if response.status_code == 201:
        print("user added successfully")
    else:
        print("failed to add user", response.status_code, response.text)

    print(f"time processing for {len(users_list)} users is :{datetime.now() - start_time}")

    return response

def set_users():
    futures = list()
    for i in range(0, len(users_list), 20):
        batch_data = users_list[i:i + 20]
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures.append(executor.submit(users_batch, batch_data))

    for future in as_completed(futures):
        future.result()
def get_user(user_id):
    response = r.get(urljoin(url, f"/users/{user_id}"),
                     headers={"x-okapi-token": token, "Content-Type": "application/json"})
    if response.status_code == 200:
        print(response.json())
    else:
        print("cant find user" + user_id, response.status_code, response.text)
        return None

# write the users to folio
start_time = datetime.now()
set_users()
print(f"set_users with concurrent threads ended after {datetime.now() - start_time}")
# Now we check if they are stored in folio

users_id_list = get_all_user_ids()
for user_id in users_id_list:
    get_user(user_id)
