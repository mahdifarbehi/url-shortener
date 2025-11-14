from typing import TypeVar

from sqlalchemy.orm.session import Session

from core.exceptions import NotFoundException

T = TypeVar("T")


class MainRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, object) -> None:
        self.session.add(object)

    def get_one(self, cls: type[T], **kwargs) -> T:
        obj = self.session.query(cls).filter_by(**kwargs, deleted_at=None).one_or_none()
        if obj is None:
            raise NotFoundException(cls_name=cls.__name__)
        return obj

    def get_all(self, cls: type[T], **kwargs) -> list[T]:
        return self.session.query(cls).filter_by(**kwargs, deleted_at=None).all()
