from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSConfig(BaseSettings):
    """
    Pydantic class for pulling/storing CORS middleware configuration settings.
    Check ``template.env`` for expected .env keys.
    """

    model_config = SettingsConfigDict(env_prefix="CORS_")
    # TODO: (STEP 6) Implement this stub!


def add_cors_middleware(app: FastAPI) -> None:
    """
    Adds the cors middleware to the FastAPI app

    :param app: FastAPI app to add the middleware to
    """
    # TODO: (STEP 6) Update this function to properly attach the CORS middleware.
    cors_settings = CORSConfig()
    print(f"CORSConfig not implemented. ({cors_settings})")
    app.add_middleware(
        CORSMiddleware,
    )
