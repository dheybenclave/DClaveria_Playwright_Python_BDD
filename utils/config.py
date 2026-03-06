import os


class Config:
    """
    Centralized configuration for the framework.
    Supports role-based credentials (e.g., ADMIN, USER).
    """
    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
    API_BASE_URL = f"{BASE_URL}/api"

    @classmethod
    def get_credentials_env(cls, role: str):
        """
        Fetches credentials based on role (admin/user).
        Expects .env keys like: ADMIN_EMAIL, ADMIN_PASSWORD, USER_EMAIL, USER_PASSWORD
        """
        role = role.upper()
        email = os.getenv(f"{role}_EMAIL")
        password = os.getenv(f"{role}_PASSWORD")

        if not email or not password:
            raise EnvironmentError(
                f"CRITICAL: Credentials for role '{role}' not found in .env."
            )

        return {"email": email, "password": password}

    @classmethod
    def validate_config(cls):
        """Ensures critical base variables are set."""
        if not cls.BASE_URL:
            raise EnvironmentError("CRITICAL: BASE_URL is not defined.")