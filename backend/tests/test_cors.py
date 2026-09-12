from collections.abc import AsyncIterator

import httpx
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.env_settings.cors_config import CORSConfig, add_cors_middleware
from main import app as main_app

ORIGIN = "http://frontend.test:5175"


@pytest.fixture
def cors_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ALLOW_ORIGINS", f'["{ORIGIN}"]')
    monkeypatch.setenv("CORS_ALLOW_CREDENTIALS", "true")
    monkeypatch.setenv("CORS_ALLOW_METHOD", '["GET", "POST"]')
    monkeypatch.setenv("CORS_ALLOW_HEADERS", '["X-Custom"]')


@pytest.fixture
async def client(cors_env: None) -> AsyncIterator[httpx.AsyncClient]:
    """A bare app with one route and the CORS middleware configured from the env above."""
    app = FastAPI()
    app.get("/ping")(lambda: {"ok": True})
    add_cors_middleware(app)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


def test_config_reads_cors_env(cors_env: None) -> None:
    config = CORSConfig()
    assert config.allow_origins == [ORIGIN]
    assert config.allow_credentials is True


def test_main_app_has_cors_middleware() -> None:
    assert any(m.cls is CORSMiddleware for m in main_app.user_middleware)


async def test_allowed_origin_gets_cors_headers(client: httpx.AsyncClient) -> None:
    response = await client.get("/ping", headers={"Origin": ORIGIN})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN
    assert response.headers["access-control-allow-credentials"] == "true"


async def test_other_origin_gets_no_cors_headers(client: httpx.AsyncClient) -> None:
    response = await client.get("/ping", headers={"Origin": "http://evil.test"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


async def test_preflight_allows_configured_method_and_header(client: httpx.AsyncClient) -> None:
    response = await client.options(
        "/ping",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-Custom",
        },
    )
    assert response.status_code == 200
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "x-custom" in response.headers["access-control-allow-headers"].lower()


async def test_preflight_rejects_unconfigured_method(client: httpx.AsyncClient) -> None:
    response = await client.options(
        "/ping",
        headers={"Origin": ORIGIN, "Access-Control-Request-Method": "DELETE"},
    )
    assert response.status_code == 400
