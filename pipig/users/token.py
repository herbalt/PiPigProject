from itsdangerous import URLSafeTimedSerializer
from credentials import credentials

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(credentials.SECRET_KEY)
    return serializer.dumps(email, salt=credentials.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(credentials.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=credentials.SECURITY_PASSWORD_SALT, max_age=expiration)
    except:
        return False
    return email
