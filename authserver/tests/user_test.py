import json
from app.services.auth import auth_service

email = "lebronjames@gmail.com"

firebase_data = {
    "email": email,
    "uid": "E90qRcXZLbP6QdzcrJrn0fmz5Um1",
}

API_KEY = "ULTRAMEGAFAKEAPIKEY"

X_ACCESS_TOKEN = 'WlxyCjKBDOfjJAbW800G57o4e' \
                 'BIpe3nJwTiPrJJgeTnTX0RPzc' \
                 '0XxZkG0y2QGkJOr9Pu3V8unfk' \
                 'p0xhFx9b802G3gPsJ150USj1T' \
                 '0C9Nvi1Gy4GRz3FyaBgPoPXg'


header = {"api-key": API_KEY, "x-access-token": X_ACCESS_TOKEN}


def test_add_registered_user(test_app):
    auth_service.set_user_data(firebase_data)

    registered_user_payload = {
        "email": email
    }

    response = test_app.post(url="/user/registered",
                             headers=header,
                             data=json.dumps(registered_user_payload))

    assert response.status_code == 201

    response_json = response.json()

    assert response_json["uuid"] == 1
    assert response_json["email"] == email


def test_add_registered_user_with_duplicated_email(test_app):
    duplicated_registered_user_payload = {
        "email": email
    }

    response = test_app.post(url="/user/registered",
                             headers=header,
                             data=json.dumps(duplicated_registered_user_payload))

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["error"] == f"email {email} already in use"


def test_add_registerd_user_with_invalid_token(test_app):
    auth_service.set_invalid_token()

    registered_user_payload = {
        "email": email
    }

    response = test_app.post(url="/user/registered",
                             headers=header,
                             data=json.dumps(registered_user_payload))

    assert response.status_code == 401

    response_json = response.json()

    assert response_json["error"] == "invalid token"


def test_get_user_from_token(test_app):
    auth_service.set_valid_token()

    response = test_app.get(url="/user/id",
                            headers=header)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["uuid"] == 1
    assert response_json["email"] == email


def test_get_user_from_invalid_token(test_app):
    auth_service.set_invalid_token()

    response = test_app.get(url="/user/id",
                            headers=header)

    assert response.status_code == 401

    response_json = response.json()

    assert response_json["error"] == "invalid token"

