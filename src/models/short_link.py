from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sao

from db.base import Base


class ShortLink(Base):
    __tablename__ = "short_links"

    short_code: sao.Mapped[str] = sao.mapped_column(
        sa.String(20), unique=True, index=True
    )
    target_url: sao.Mapped[str] = sao.mapped_column(sa.String())
    click_count: sao.Mapped[int] = sao.mapped_column(sa.Integer, default=0)

    def to_dict(self) -> dict[str, str | int | datetime]:
        return {
            "id": self.id,
            "short_code": self.short_code,
            "target_url": self.target_url,
            "click_count": self.click_count,
            "created_at": self.created_at,
        }
