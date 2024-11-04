import pyotp
import redis
from decouple import config
from django_otp.oath import totp


REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def generate_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=6)

    otp = totp.now()

    # Keep generating OTP until it does not start with zero
    while otp.startswith('0'):
        otp = totp.now()

    return otp

def generate_and_store_otp(user_id, otp_expiry=300):
    otp = generate_otp()
    redis_client.setex(f'otp:{user_id}', otp_expiry, otp)

    return otp

def verify_otp(user_id, otp):
    stored_otp = redis_client.get(f'otp:{user_id}')
    if stored_otp and stored_otp.decode() == otp:
        redis_client.delete(f'otp:{user_id}')
        return True
    else:
        return False