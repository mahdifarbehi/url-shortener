import secrets
import string
from typing import Any

from db.unit_of_work import UnitOfWork
from dtos.request_models import CreateShortLinkRequestModel
from models.short_link import ShortLink


def generate_short_code() -> str:
    characters = string.ascii_letters + string.digits
    short_code = "".join(secrets.choice(characters) for _ in range(10))
    print(short_code)
    return short_code


def create_short_link_handler(
    uow: UnitOfWork, data: CreateShortLinkRequestModel
) -> dict[str, Any]:
    with uow:
        short_link = ShortLink(
            short_code=generate_short_code(), target_url=data.original_url
        )
        uow.main_repo.add(short_link)
        uow.commit()
        return short_link.to_dict()
