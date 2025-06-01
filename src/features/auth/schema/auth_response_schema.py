from pydantic import BaseModel


class AuthResponseModel(BaseModel):
    access_token: str
    token_type: str
