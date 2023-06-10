import pynecone as pc
from passlib.context import CryptContext

from app.backend import crud
from app.backend.models import User
from typing import Optional

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# From FastAPI's OAuth2 example: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(
    email: str, password: str, db: pc.session
) -> tuple[bool, Optional[User]]:
    user = crud.get_user(db=db, email=email, with_password=True)
    if not user:
        return False, None
    if not verify_password(password, user.hashed_password):
        return False, None
    return True, user
