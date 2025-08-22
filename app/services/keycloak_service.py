import logging

from fastapi import HTTPException
from keycloak import KeycloakAdmin, KeycloakOpenID
from fastapi import status
from app.core.config import settings
from app.schemas.user_schema import UserRequest
import requests


import logging

logger = logging.getLogger(__name__)

class KeycloakService:
    def __init__(self):
        token_url = f"{settings.keycloak_server_url}realms/{settings.keycloak_realm}/protocol/openid-connect/token"
        data = {
            "client_id": settings.keycloak_client_id,
            "client_secret": settings.keycloak_client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Keycloak token fetch failed: {response.text}")

        token_dict = response.json()

        # ✅ Pass the whole token dict, not just access_token
        self.admin_client = KeycloakAdmin(
            server_url=settings.keycloak_server_url,
            realm_name=settings.keycloak_realm,
            token=token_dict,
            verify=True
        )

        # OpenID client for login and token verification
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.keycloak_server_url,
            client_id=settings.keycloak_public_client_id,
            realm_name=settings.keycloak_realm,
            client_secret_key=settings.keycloak_client_secret
        )

    def create_user(self,user_data:dict):

        try:
            existing_users=self.admin_client.get_users({"username":user_data["email"]})
            if existing_users:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User already exists in keycloak"
                )

            user_id=self.admin_client.create_user(user_data)
            logger.info(f"User created in Keycloak with ID: {user_id}")
            return user_id

        except Exception as e:
            logger.error(f"Failed to create user in Keycloak :{str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user in Keycloak"
            )

