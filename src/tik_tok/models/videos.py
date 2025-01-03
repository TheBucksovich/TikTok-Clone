from datetime import datetime
from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped

from tik_tok.models.base import Base


class Video(Base):
    __tablename__ = "videos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    file_url: Mapped[str] = mapped_column(nullable=False)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(nullable=True)  # Make it optional
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)