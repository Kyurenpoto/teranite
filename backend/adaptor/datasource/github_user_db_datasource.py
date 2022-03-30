from adaptor.datasource.github_user_datasource import GithubUserDataSource
from database import Base
from dependency import provider
from sqlalchemy import Column, String


class UserTable(Base):
    __tablename__ = "User"

    email = Column(String, primary_key=True, nullable=False, unique=True)
    github_access_token = Column(String, primary_key=True, nullable=False, unique=True)
    github_refresh_token = Column(String, primary_key=True, nullable=False, unique=True)


class GithubUserDBDataSource(GithubUserDataSource):
    async def readUser(self, email: str) -> dict | None:
        match provider["db"].db.query(UserTable).filter(UserTable.email == email).first():
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
        
        db = provider["db"].db
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    async def updateUser(self, email: str, accessToken: str, refreshToken: str):
        db = provider["db"].db
        db.query(UserTable).filter(UserTable.email == email).update(
            {"github_access_token": accessToken, "github_refresh_token": refreshToken}
        )
        db.commit()
