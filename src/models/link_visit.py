from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sao

from db.base import Base


class LinkVisit(Base):
    __tablename__ = "link_visits"

    short_link_id: sao.Mapped[int] = sao.mapped_column(
        sa.Integer, sa.ForeignKey("short_links.id"), index=True
    )
    client_ip: sao.Mapped[str] = sao.mapped_column(sa.String())
    timestamp: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)

    def to_dict(self) -> dict[str, str | int | datetime]:
        return {
            "id": self.id,
            "short_link_id": self.short_link_id,
            "client_ip": self.client_ip,
            "timestamp": self.timestamp,
        }
