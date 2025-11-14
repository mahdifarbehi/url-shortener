from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sao


class Base(sao.DeclarativeBase):
    
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    created_at: sao.Mapped[datetime] = sao.mapped_column(default=sa.func.now())
    updated_at: sao.Mapped[datetime] = sao.mapped_column(
        default=sa.func.now(), onupdate=sa.func.now()
    )
    deleted_at: sao.Mapped[datetime | None] = sao.mapped_column(nullable=True)
