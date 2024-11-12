from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.models import ModelMixin


class UserModel(ModelMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    token: Mapped[list["JWTModel"]] = relationship("JWTModel", back_populates="user")


class JWTModel(ModelMixin):
    __tablename__ = "jwt"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[UserModel] = relationship("UserModel", back_populates="tokens")
