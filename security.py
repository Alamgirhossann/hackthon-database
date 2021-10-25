import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from config import API_CONFIG_DEFAULT_USERNAME, API_CONFIG_DEFAULT_PASSWORD

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, API_CONFIG_DEFAULT_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, API_CONFIG_DEFAULT_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
