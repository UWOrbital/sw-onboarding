from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict


# wiring is already there -> main.py calls setup_middlewares calls add_cors_middleware
# make corsconfig read the four evironment variables and pass them into corsmiddleware
# cors -> Cross-Origin Resource Sharing -> http-header mechanism (fastapi uses corsmiddleaware)
class CORSConfig(BaseSettings):
    """
    Pydantic class for pulling/storing CORS middleware configuration settings.
    Check ``template.env`` for expected .env keys.
    """

    model_config = SettingsConfigDict(env_prefix="CORS_")
    # template.env uses COWS_ALLOW_METHOD with env_prefix="CORS"
    allow_origins: list[str]
    allow_credentials: bool
    allow_method: list[str]
    allow_headers: list[str]

    # (STEP 5) Implement this stub!


def add_cors_middleware(app: FastAPI) -> None:
    """
    Adds the cors middleware to the FastAPI app

    :param app: FastAPI app to add the middleware to
    """
    # (STEP 5) Update this function to properly attach the CORS middleware. (6 tests passed)
    cors_settings = CORSConfig()
    # print(f"CORSConfig not implemented. ({cors_settings})")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.allow_origins,
        allow_credentials=cors_settings.allow_credentials,
        allow_methods=cors_settings.allow_method,
        allow_headers=cors_settings.allow_headers,
    )
