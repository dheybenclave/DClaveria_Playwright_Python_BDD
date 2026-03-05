import os

from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()


class Config:
    """
    Centralized configuration for the framework.
    Fetches values from .env or environment variables.
    """
    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")

    # api_suites Configuration
    API_BASE_URL = f"{BASE_URL}/api"

    @classmethod
    def validate_config(cls):
        """Ensures critical variables are set before running test"""
        if not cls.USER_EMAIL or not cls.USER_PASSWORD:
            raise EnvironmentError(
                "CRITICAL: USER_EMAIL or USER_PASSWORD not found in .env file or environment variables."
            )
