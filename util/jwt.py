import jwt 
from util import apiKey 

SECRET_KEY = apiKey.getApiKey("JWT_SECET_KEY")

def checkJWTToken(token):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"success":True, "message": "Access granted", "decode": decode}
    except jwt.ExpiredSignatureError:
        return {"success":False,"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"success":False,"error": "Invalid token"}