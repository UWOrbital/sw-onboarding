from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSConfig(BaseSettings):
    """
    Pydantic class for pulling/storing CORS middleware configuration settings.
    Check ``template.env`` for expected .env keys.

    Defaults are the closed configuration: no origins allowed, no credentials.
    """

    model_config = SettingsConfigDict(env_prefix="CORS_", extra="ignore")

    allow_origins: list[str] = []
    allow_credentials: bool = False
    allow_method: list[str] = ["*"]  # singular, to match CORS_ALLOW_METHOD in template.env
    allow_headers: list[str] = ["*"]


def add_cors_middleware(app: FastAPI) -> None:
    """
    Adds the cors middleware to the FastAPI app

    :param app: FastAPI app to add the middleware to
    """
    cors_settings = CORSConfig()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.allow_origins,
        allow_credentials=cors_settings.allow_credentials,
        allow_methods=cors_settings.allow_method,
        allow_headers=cors_settings.allow_headers,
    )
