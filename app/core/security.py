from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fetch public key from Keycloak
def get_public_key():
    url = f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    resp = requests.get(url).json()
    return resp["keys"][0]  # Simplified: handle multiple keys in production

def decode_token(token: str):
    try:
        key = get_public_key()
        return jwt.decode(token, key, algorithms=[settings.ALGORITHM], audience=settings.KEYCLOAK_CLIENT_ID)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return payload

def require_role(role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        roles = user.get("realm_access", {}).get("roles", [])
        if role not in roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker
