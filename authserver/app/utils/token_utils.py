from app.services.auth import auth_service

def check_token(token):
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token:
        raise MissingTokenError();

    return auth_service.verify_id_token(token)
    