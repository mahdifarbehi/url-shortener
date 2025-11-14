import inspect
from datetime import datetime
from functools import wraps

from fastapi import Request

from core.exceptions import BadRequestException
from core.logger import AppLogger
from db.unit_of_work import UnitOfWork
from models.link_visit import LinkVisit
from models.short_link import ShortLink

logger = AppLogger(__name__)


def get_client_ip(request: Request) -> str:

    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
        if ip:
            return ip

    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip.strip()

    return "unknown"


def create_link_visit_handler(uow: UnitOfWork, short_code: str, client_ip: str) -> None:
    with uow:
        short_link = uow.main_repo.get_one(ShortLink, short_code=short_code)
        short_link.click_count += 1
        link_visit = LinkVisit(
            short_link_id=short_link.id, client_ip=client_ip, timestamp=datetime.now()
        )
        uow.main_repo.add(link_visit)
        uow.commit()
        logger.info(
            f"Link visit recorded. ip: {client_ip}, timestamp: {link_visit.timestamp}",
        )


def log_client_usage():

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            request: Request | None = kwargs.get("request")
            uow: UnitOfWork | None = kwargs.get("uow")
            short_code: str | None = kwargs.get("short_code")
            if not request or not uow or not short_code:
                raise BadRequestException(
                    "Request, UnitOfWork, or short_code object is missing"
                )

            client_ip = get_client_ip(request)
            create_link_visit_handler(uow, short_code, client_ip)

            return result

        wrapper.__signature__ = inspect.signature(func)  # type: ignore

        return wrapper

    return decorator
