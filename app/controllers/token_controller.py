from fastapi import APIRouter, HTTPException, Form
import requests
from app.core.config import settings

router = APIRouter()


@router.post("/token")
def get_token(username: str, password: str):
    token_url = f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"

    data = {
        "grant_type": "password",
        "client_id": settings.keycloak_public_client_id,
        "username": username,
        "password": password,
    }

    # if client is confidential
    if settings.keycloak_client_secret:
        data["client_secret"] = settings.keycloak_client_secret

    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()