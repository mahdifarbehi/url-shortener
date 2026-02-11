import secrets

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi import HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.log_decorator import log_client_usage
from db.unit_of_work import UnitOfWork, get_uow
from dtos.request_models import CreateShortLinkRequestModel
from services.create_short_link import create_short_link_handler
from services.get_stats import get_stats_handler
from services.get_url import get_url_handler

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
security = HTTPBasic(realm="URL Shortener")
DOCS_USERNAME = "admin"
DOCS_PASSWORD = "8L5JDjUuu63K"


def require_docs_auth(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    is_correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid docs credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


protected_router = APIRouter(dependencies=[Depends(require_docs_auth)])


@protected_router.get("/health")
async def read_root():
    return {"msg": "API is running"}


@protected_router.post("/shorten")
def create_short_link_api(
    data: CreateShortLinkRequestModel, uow: UnitOfWork = Depends(get_uow)
):
    return create_short_link_handler(uow=uow, data=data)


@protected_router.get("/docs", include_in_schema=False)
def swagger_ui() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")


@protected_router.get("/openapi.json", include_in_schema=False)
def openapi():
    return app.openapi()


@protected_router.get("/stats/{short_code}")
def get_stats_api(short_code: str, uow: UnitOfWork = Depends(get_uow)):

    return {"click_count": get_stats_handler(uow=uow, short_code=short_code)}


app.include_router(protected_router)


@app.get("/{short_code}", response_class=RedirectResponse)
@log_client_usage()
def get_url_api(
    request: Request,
    short_code: str,
    uow: UnitOfWork = Depends(get_uow),
):
    return get_url_handler(uow=uow, short_code=short_code)
