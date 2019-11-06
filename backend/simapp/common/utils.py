import requests
import json

ROLES = (
    ('ADMIN', 'ADMIN'),
    ('CUSTOMER', 'CUSTOMER'),
    ('DOCTOR', 'DOCTOR'),
    ('MANAGER', 'MANAGER'),

)

DEFAULT_USER_ROLE = 'CUSTOMER'

LANGUAGES = (
    ('En', 'English'),
    ('He', 'Hebrew'),
    ('Fr', 'Français'),
    ('Ge', 'Deutsche'),
    ('It', 'Italiano'),
    ('Sp', 'Español'),
    ('Ru', 'Russian')

)

DEFAULT_LANGUAGE = LANGUAGES[0][0]


def send_pushes(players_ids,text,tittle):
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": "c765d70d-0b23-4735-9e92-6ba05f741e85",
               "include_player_ids": players_ids,
               "contents": {"en": text},
               "headings": {"en": tittle}

               }
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

