from fastapi import HTTPException,status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
import requests
from sqlalchemy.orm import Session
from app.core.config import settings, keycloak_openid
from jose import jwt, JWTError
from app.database import get_db
from app.models.user import User

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_jwks():
    url = f"{settings.keycloak_server_url}realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    return requests.get(url).json()

JWKS=get_jwks()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Get public key
        public_key = keycloak_openid.public_key()
        key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=f"{settings.keycloak_server_url}realms/{settings.keycloak_realm}",
            options={"verify_aud": False}
        )

        # Extract roles
        roles = []
        realm_access = payload.get("realm_access", {})
        roles.extend(realm_access.get("roles", []))

        resource_access = payload.get("resource_access", {})
        client_roles = resource_access.get(settings.keycloak_client_id, {})
        roles.extend(client_roles.get("roles", []))

        return payload

    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def require_role(role: str):
    def role_checker(payload=Depends(verify_token), db: Session = Depends(get_db)):
        # Token থেকে email নিন
        user_email = payload.get("email")

        if not user_email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        # Database থেকে user find করুন email দিয়ে
        user = db.query(User).filter(User.email == user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # User এর roles check করুন (roles একটা list)
        user_roles = user.roles  # ["USER", "ADMIN"]

        if role.upper() not in [r.upper() for r in user_roles]:
            raise HTTPException(status_code=403, detail=f"Requires '{role}' role")

        return user  # শুধু user return করছি

    return role_checker