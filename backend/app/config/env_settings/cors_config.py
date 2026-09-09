from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings


class CORSConfig(BaseSettings):
    """
    Pydantic class for pulling/storing CORS middleware configuration settings.
    Check `.env.example` for expected .env keys.
    """

    # TODO: Implement this stub!


def add_cors_middleware(app: FastAPI) -> None:
    """
    Adds the cors middleware to the FastAPI app

    :param app: FastAPI app to add the middleware to
    """
    cors_settings = CORSConfig()
    print(f"CORSConfig not implemented. ({cors_settings})")
    app.add_middleware(
        CORSMiddleware,
    )
