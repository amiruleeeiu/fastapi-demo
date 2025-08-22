from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Keycloak Example"
    KEYCLOAK_SERVER_URL: str = "http://localhost:8080/auth/"
    KEYCLOAK_REALM: str = "myrealm"
    KEYCLOAK_CLIENT_ID: str = "fastapi-client"
    KEYCLOAK_CLIENT_SECRET: str = "supersecret"
    ALGORITHM: str = "RS256"

    class Config:
        env_file = ".env"

settings = Settings()
