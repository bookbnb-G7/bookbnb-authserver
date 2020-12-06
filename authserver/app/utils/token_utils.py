from app.services.auth import auth_service

def check_token(token):
    if not token:
        raise MissingTokenError();

    return auth_service.verify_id_token(token)
    