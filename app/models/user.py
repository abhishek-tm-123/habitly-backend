from app.db.base import Base

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped,mapped_column,relationship

if TYPE_CHECKING:
    from app.models.habit import Habit

class User(Base):

    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True,index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,

    )

    habits: Mapped[list["Habit"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
    )

