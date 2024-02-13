import pandas as pd
from uuid import uuid4
from datetime import datetime
import requests as r
import folio_auth

def generate_users(groups=True):
    dict_groups={}
    file_path = r"C:\Users\tajini.NB419\PycharmProjects\adresstypes\Data\testdaten.csv"
    fieldnames = ["group", "barcode", "geschlecht", "lastname", "firstname", "dateOfBirth", "expirationDate", "gesch",
                  "nummer", "countryid", "region", "addressLine1", "postalCode", "adressLine2", "email", "barcode2"]
    df = pd.read_csv(r"C:\Users\tajini.NB419\PycharmProjects\adresstypes\Data\testdaten.csv", names=fieldnames)
    df["addressLine1"] = df["addressLine1"] + " " + df["adressLine2"].astype(str)
    df["lastname"] = df["geschlecht"] + " " + df["lastname"]
    df.drop(columns=["adressLine2"], inplace=True)
    df.drop(columns=["geschlecht"], inplace=True)
    df.to_csv('new_file.csv', header=True, index=False)
    # print("df len",len(df))
    user_list = list()
    if groups:
        values=set(df["group"].values.tolist())
        for x in values:
            id=str(uuid4())
            dict_groups.update({str(x): id})
            response=r.post(url="https://folio-snapshot-okapi.dev.folio.org/groups",
               headers={"x-okapi-token": folio_auth.get_token()
                   , "Content-Type": "application/json"}, json={
                "group": f"Group {x}",
                "expirationOffsetInDays": 365,
                "id": id,
            })
            if response.ok:
                print("Group created successfully")
            else:
                print(response.status_code, response.text)
    for i in range(len(df)):
        user_id = str(uuid4())
        barcode = str(df["barcode"][i])
        expiration_date = datetime.strptime(str(df["expirationDate"][i]),"%Y%m%d")
        birth_date = datetime.strptime(str(df["dateOfBirth"][i]), "%Y%m%d")
        ###
        user = {
            "id": user_id,
            "barcode": barcode,
            #"active": random.choice([True, False]),
            "personal": {
                "lastName": df["lastname"][i],
                "firstName": df["firstname"][i],
                "email": df["email"][i],
                "dateOfBirth": birth_date.strftime("%Y-%m-%d"),
                "addresses": [
                    {
                        "countryId": df["countryid"][i],
                        "addressLine1": df["addressLine1"][i],
                        "region": df["region"][i],
                        "postalCode": df["postalCode"][i],
                        "addressTypeId": "93d3d88d-499b-45d0-9bc7-ac73c3a19880",
                        "primaryAddress": True
                    }
                ]
            },
            "expirationDate": expiration_date.strftime("%Y-%m-%d")
        }
        if groups:
            #user["patronGroup"] = "Group "+ str(df["group"][i])
            user["patronGroup"]=dict_groups[str(df["group"][i])]

        user_list.append(user)



    return user_list