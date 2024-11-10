from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.models import ModelMixin


class UserModel(ModelMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
