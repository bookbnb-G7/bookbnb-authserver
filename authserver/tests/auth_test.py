from app.services.auth import auth_service

API_KEY = "ULTRAMEGAFAKEAPIKEY"

X_ACCESS_TOKEN = (
    "WlxyCjKBDOfjJAbW800G57o4e"
    "BIpe3nJwTiPrJJgeTnTX0RPzc"
    "0XxZkG0y2QGkJOr9Pu3V8unfk"
    "p0xhFx9b802G3gPsJ150USj1T"
    "0C9Nvi1Gy4GRz3FyaBgPoPXg"
)

header = {"api-key": API_KEY, "x-access-token": X_ACCESS_TOKEN}


def test_logged_user(test_app):
    auth_service.set_valid_token()

    response = test_app.post(url="/auth/sign-in", headers=header)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["message"] == "ok"


def test_user_with_expired_token(test_app):
    auth_service.set_expired_token()

    response = test_app.post(url="/auth/sign-in", headers=header)

    assert response.status_code == 401

    response_json = response.json()

    assert response_json["error"] == "token has expired"


def test_user_with_revoked_token(test_app):
    auth_service.set_revoked_token()

    response = test_app.post(url="/auth/sign-in", headers=header)

    assert response.status_code == 401

    response_json = response.json()

    assert response_json["error"] == "token has been revoked"


def test_user_with_invalid_token(test_app):
    auth_service.set_invalid_token()

    response = test_app.post(url="/auth/sign-in", headers=header)

    assert response.status_code == 401

    response_json = response.json()

    assert response_json["error"] == "invalid token"


def test_user_without_token(test_app):
    auth_service.set_valid_token()

    header_without_token = {"api-key": API_KEY}

    response = test_app.post(url="/auth/sign-in", headers=header_without_token)

    assert response.status_code == 400

    response_json = response.json()

    assert response_json["error"] == "missing token"
