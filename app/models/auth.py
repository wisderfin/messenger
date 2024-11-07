from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_model import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
        )
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
        )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
        )
    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
        )
