import random
from datetime import datetime, timedelta
from uuid import uuid4

from faker import Faker

# groups can be found here :https://github.com/folio-org/mod-users/tree/master/src/main/resources/ref-data/groups-17.3.0
groups = ["503a81cd-6c26-400f-b620-14c08943697c",
          "ad0bc554-d5bc-463c-85d1-5562127ae91b",
          "3684a786-6671-4268-8ed0-9db82ebca60b",
          "bdc2b6d4-5ceb-4a12-ab46-249b9a68473e"]

# adresstypes id can be found at : https://github.com/folio-org/mod-users/tree/master/src/main/resources/ref-data/addresstypes-15.4.0
address_types_id = ["b6f4d1c6-0dfa-463c-9534-f49c4f0ae090",
                    "93d3d88d-499b-45d0-9bc7-ac73c3a19880",
                    "46ff3f08-8f41-485c-98d8-701ba8404f4f",
                    "a3c3d60b-df9e-41d9-b7f5-983008bc1a45",
                    "c42be2ab-c3fd-486c-a1fe-9e5ea0f16198",
                    "1c4b225f-f669-4e9b-afcd-ebc0e273a34e"]

country_code = "DE"
contacts = ['001', '002', '003', '004', '005']
fake = Faker('de_DE')


def generate_fake_user(users):
    user_list = list()
    for i in range(users):
        user_id = str(uuid4())
        username = fake.user_name()
        barcode = str(random.randint(10 ** 14, 10 ** 19 - 1))
        enrollment_date = datetime.now() - timedelta(weeks=int(random.random() * 20))
        expiration_date = datetime.now() + timedelta(weeks=int(random.random() * 120))

        start_year = 1990
        end_year = 2003
        birth_date = datetime(
            year=start_year + int(random.random() * (end_year - start_year + 1)),
            month=random.randint(1, 12),
            day=random.randint(1, 28))

        ###
        user = {
            "username": username,
            "id": user_id,
            "barcode": barcode,
            "active": random.choice([True, False]),
            "personal": {
                "lastName": Faker().last_name(),
                "firstName": fake.first_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "dateOfBirth": birth_date.strftime("%Y-%m-%d"),
                "preferredContactTypeId": random.choice(contacts),
                "addresses": [
                    {
                        "countryId": country_code,
                        "addressLine1": fake.street_address(),
                        "city": fake.city(),
                        "region": fake.state(),
                        "postalCode": fake.postcode(),
                        "addressTypeId": random.choice(address_types_id),
                        "primaryAddress": True
                    }
                ]
            },
            "enrollmentDate": enrollment_date.strftime("%Y-%m-%d"),
            "expirationDate": expiration_date.strftime("%Y-%m-%d")
        }
        user_list.append(user)
    return user_list
