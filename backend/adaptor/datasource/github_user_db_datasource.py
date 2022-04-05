from adaptor.datasource.github_user_datasource import GithubUserDataSource
from database import Base
from dependencies.dependency import provider
from sqlalchemy import Column, String


class UserTable(Base):
    __tablename__ = "User"

    email = Column(String, primary_key=True, nullable=False, unique=True)
    github_access_token = Column(String, primary_key=True, nullable=False, unique=True)
    github_refresh_token = Column(String, primary_key=True, nullable=False, unique=True)


class GithubUserDBDataSource(GithubUserDataSource):
    def __init__(self):
        self.db = provider["auth"]["db"].db
    
    async def readUser(self, email: str) -> dict | None:
        match self.db.query(UserTable).filter(UserTable.email == email).first():
            case UserTable(email=userEmail, github_access_token=accessToken, github_refresh_token=refreshToken):
                return {
                    "email": str(userEmail),
                    "githubAccessToken": str(accessToken),
                    "githubRefreshToken": str(refreshToken)
                }
            
        return None

    async def createUser(self, email: str, accessToken: str, refreshToken: str):
        db_user = UserTable(
            email=email,
            github_access_token=accessToken,
            github_refresh_token=refreshToken,
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

    async def updateUser(self, email: str, accessToken: str, refreshToken: str):
        self.db.query(UserTable).filter(UserTable.email == email).update(
            {"github_access_token": accessToken, "github_refresh_token": refreshToken}
        )
        self.db.commit()
