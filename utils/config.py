import json
import logging
import os


class Config:
    """
    Centralized configuration for the framework.
    Supports role-based credentials (e.g., ADMIN, USER).
    """
    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
    API_BASE_URL = f"{BASE_URL}/api"

    @classmethod
    def get_credentials(cls, role: str):
        raw_json = os.getenv("LIST_OF_CREDENTIALS")

        # 1. Try JSON secret (CI/CD)
        if raw_json:
            try:
                creds_data = json.loads(raw_json)
                role_creds = creds_data.get(role.lower())

                if role_creds:
                    # Updated to use 'pw' as per your secret structure
                    return {
                        "email": role_creds.get("email"),
                        "password": role_creds.get("password")
                    }
                logging.warning(f"Role '{role}' not found in LIST_OF_CREDENTIALS.")
            except json.JSONDecodeError:
                logging.error("LIST_OF_CREDENTIALS is not valid JSON.")

        # 2. Fallback to .env (Local Dev)
        email = os.getenv(f"{role.upper()}_EMAIL")
        password = os.getenv(f"{role.upper()}_PASSWORD")

        if email and password:
            return {"email": email, "password": password}

        raise EnvironmentError(f"Credentials for '{role}' not found in Secret or .env")

    @classmethod
    def validate_config(cls):
        """Ensures critical base variables are set."""
        if not cls.BASE_URL:
            raise EnvironmentError("CRITICAL: BASE_URL is not defined.")
