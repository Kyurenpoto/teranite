from pydantic import BaseModel


class User(BaseModel):
    email: str
    githubAccessToken: str
    githubRefreshToken: str

    class Config:
        orm_mode = True
