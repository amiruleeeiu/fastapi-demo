import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Keycloak Configuration
    keycloak_server_url: str = "https://alpha-idp.oss.net.bd/"
    keycloak_realm: str = "iba-alumni-club"
    keycloak_client_id: str = "iba-resource"
    keycloak_client_secret: str = "a1fkyky61hwUInjE5SsZOvqnYgWXvBT8"
    keycloak_public_client_id: str = "iba-public"
    keycloak_admin_password: str = "12345"
    DEFAULT_PASSWORD:str ="12345"
    # Database Configuration

    database_url: str = "postgresql://user:password@localhost/dbname"

    # API Configuration
    api_title: str = "Keycloak User Management API"
    api_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()