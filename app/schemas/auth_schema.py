from pydantic import BaseModel


class TokenRequest(BaseModel):
    username:str
    password:str

class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str='bearer'
    expires_in: int

class UserRegistration(BaseModel):
    username:str
    password:str
    email:str
    first_name:str
    last_name:str

