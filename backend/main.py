from fastapi import FastAPI

from app.config.backend_setup import setup_logging, setup_middlewares, setup_routes

app = FastAPI()
setup_logging()
setup_routes(app)
setup_middlewares(app)
