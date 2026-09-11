from dotenv import load_dotenv

from app.config.env_settings.cors_config import CORSConfig
from app.config.env_settings.database_config import DatabaseConfig

load_dotenv()


class BackendConfiguration:
    """
    Class for storing backend configuration settings
    """

    def __init__(self) -> None:
        self.cors = CORSConfig()
        self.db = DatabaseConfig()


settings = BackendConfiguration()
