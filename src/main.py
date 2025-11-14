from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse

from core.log_decorator import log_client_usage
from db.unit_of_work import UnitOfWork, get_uow
from dtos.request_models import CreateShortLinkRequestModel
from services.create_short_link import create_short_link_handler
from services.get_stats import get_stats_handler
from services.get_url import get_url_handler

app = FastAPI()


@app.get("/health")
async def read_root():
    return {"msg": "API is running"}


@app.post("/shorten")
def create_short_link_api(
    data: CreateShortLinkRequestModel, uow: UnitOfWork = Depends(get_uow)
):
    return create_short_link_handler(uow=uow, data=data)


@app.get("/{short_code}", response_class=RedirectResponse)
@log_client_usage()
def get_url_api(
    request: Request,
    short_code: str,
    uow: UnitOfWork = Depends(get_uow),
):
    return get_url_handler(uow=uow, short_code=short_code)


@app.get("/stats/{short_code}")
def get_stats_api(short_code: str, uow: UnitOfWork = Depends(get_uow)):

    return {"click_count": get_stats_handler(uow=uow, short_code=short_code)}
