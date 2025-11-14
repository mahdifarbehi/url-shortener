import pytest
from fastapi.testclient import TestClient

from db.base import Base
from db.orm import TEST_BIND
from db.unit_of_work import get_test_uow, get_uow
from main import app
from models.link_visit import LinkVisit  # noqa: F401
from models.short_link import ShortLink  # noqa: F401


@pytest.fixture(scope="function")
def test_client():

    Base.metadata.drop_all(bind=TEST_BIND)
    Base.metadata.create_all(bind=TEST_BIND)

    app.dependency_overrides[get_uow] = get_test_uow

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_BIND)


def test_health(test_client: TestClient):
    response = test_client.get("/health")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "API is running"}


def test_create_short_link(test_client):
    original_url = "https://docs.astral.sh/"
    response = test_client.post("/shorten", json={"original_url": original_url})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get("short_code") is not None
    assert data.get("target_url") == original_url
    assert data.get("click_count") == 0


def test_redirect_and_stats(test_client):
    original_url = "https://docs.astral.sh/"

    response = test_client.post("/shorten", json={"original_url": original_url})
    assert response.status_code == 200, response.text
    short_code = response.json()["short_code"]

    response = test_client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code in (302, 307), response.text
    assert response.headers.get("location") == original_url

    response = test_client.get(f"/stats/{short_code}")
    assert response.status_code == 200, response.text
    assert response.json() == {"click_count": 1}
