from fastapi import HTTPException,status
from fastapi.params import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
import requests
from app.core.config import settings
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_jwks():
    url = f"{settings.keycloak_server_url}realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    return requests.get(url).json()

JWKS=get_jwks()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(k for k in JWKS["keys"] if k["kid"] == unverified_header["kid"])
        payload = jwt.decode(token, key, algorithms=["RS256"], audience=settings.keycloak_client_id)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def require_role(role: str):
    def role_checker(payload=Depends(verify_token)):
        roles = payload.get("realm_access", {}).get("roles", [])
        if role not in roles:
            raise HTTPException(status_code=403, detail=f"Requires '{role}' role")
        return payload
    return role_checker