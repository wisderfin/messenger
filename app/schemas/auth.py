from pydantic import BaseModel, EmailStr, constr


class SignUpBaseSchema(BaseModel):
    pass


class SignUpInputSchema(SignUpBaseSchema):
    name: str
    username: str
    email: str
    password: constr(min_length=8)  # type: ignore


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenDataSchema(BaseModel):
    username: str | None


class CreateUserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
