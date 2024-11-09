from pydantic import EmailStr, field_validator, model_validator
from datetime import datetime
from re import fullmatch

from . import BaseScheme
from utils import patterns


class BaseUserScheme(BaseScheme):
    pass


class CreateUserScheme(BaseUserScheme):  # TODO: you is well done. proud of you
    name: str
    username: str
    email: EmailStr
    password: str

    @field_validator("name")
    def login_len(cls, v):
        if len(v) < 3:
            raise ValueError("the username length must be at least 3 characters long")

        # if name is not contains only letters
        elif not fullmatch(patterns.NAME_PATTERN, v):
            raise ValueError(
                f"a name may contain only uppercase, lowercase letters of the "
                f"Latin alphabet, hyphen and appostrophes"
            )
        return v

    @field_validator("username")
    def username_validator(cls, v):
        if len(v) < 3:
            raise ValueError("the username length must be at least 3 characters long")

        # if username is not contains only letters, numeric and underscore
        elif not fullmatch(patterns.USERNAME_PATTERN, v):
            raise ValueError(
                f"the name may contain only the letters of the Latin alphabet, "
                f"numbers and underscore"
            )
        return v.lower()

    @field_validator("password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError("the password length must be at least 8 characters long")

        # if password is not contains numeric, uppercase, lowercase and special characters
        elif not fullmatch(patterns.PASSWORD_PATTERN, v):
            raise ValueError(
                f"the password must contain uppercase and lowercase Latin characters,"
                f"numbers and special characters."
            )
        return v

    @model_validator(mode="after")
    def quality_validator(self):
        if self.username == self.password:
            raise ValueError("the password must not be equal to the username")
        elif self.name == self.password:
            raise ValueError("the password must not be equal to the name")
        elif self.email == self.password:
            raise ValueError("the password must not be equal to the email")
        return self


class OutputUserScheme(BaseUserScheme):
    id: int
    name: str
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    updated_at: datetime


class BaseJWTTokenScheme(BaseScheme):
    pass


class OutputJWTTokenScheme(BaseJWTTokenScheme):
    access_token: str
    token_type: str = "bearer"
