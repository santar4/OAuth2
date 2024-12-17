from datetime import datetime
from passlib.hash import bcrypt

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from schemas.user import UserType

from settings import Base





class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[UserType] = mapped_column(default=UserType.USER)
    bio: Mapped[str] = mapped_column(nullable=True)

    create_date: Mapped[datetime] = mapped_column(server_default=func.now())

    def __str__(self):
        return f"User: {self.email}, {self.username}"
