from core.exceptions import NotFoundException
from db.unit_of_work import UnitOfWork
from models.short_link import ShortLink


def get_stats_handler(uow: UnitOfWork, short_code: str) -> int:
    with uow:
        short_link = uow.main_repo.get_one(ShortLink, short_code=short_code)
        if not short_link:
            raise NotFoundException(cls_name=ShortLink.__name__)
        return short_link.click_count
