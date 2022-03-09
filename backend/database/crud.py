from os import access
from sqlalchemy.orm import Session

from . import models, schemas


def readUser(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def createUser(db: Session, user: schemas.User):
    db_user = models.User(
        email=user.email,
        github_access_token=user.githubAccessToken,
        github_refresh_token=user.githubRefreshToken,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def updateUser(db: Session, email: str, accessToken: str, refreshToken: str):
    db.query(models.User).filter(models.User.email == email).update(
        {"github_access_token": accessToken, "github_refresh_token": refreshToken}
    )
    db.commit()
