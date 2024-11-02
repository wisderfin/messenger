from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.dependes import Base


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
        String(255)
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=lambda: datetime.now(timezone.utc)
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )
