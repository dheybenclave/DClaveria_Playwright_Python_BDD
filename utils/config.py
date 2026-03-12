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
    def get_credentials( cls, role: str):
        """
            Fetches credentials from JSON secret (CI/CD) or falls back to local .env (Dev).
            """
        raw_json = os.getenv("LIST_OF_CREDENTIALS")

        # 1. Strategy: Try JSON Credentials (Priority for CI/CD)
        if raw_json:
            try:
                creds_data = json.loads(raw_json)
                role_creds = creds_data.get(role.lower())

                if role_creds:
                    return role_creds
                logging.warning(f"Role '{role}' not found in LIST_OF_CREDENTIALS JSON.")
            except json.JSONDecodeError:
                logging.error("LIST_OF_CREDENTIALS is not valid JSON.")

        # 2. Strategy: Fallback to individual .env variables (Local Development)
        logging.info(f"Falling back to individual environment variables for role: {role}")
        email = os.getenv(f"{role.upper()}_EMAIL")
        password = os.getenv(f"{role.upper()}_PASSWORD")

        if email and password:
            return {"email": email, "password": password}

        # 3. Final Error: If neither worked
        raise EnvironmentError(
            f"Credentials for role '{role}' could not be found in JSON secret OR local .env variables."
        )

    @classmethod
    def validate_config(cls):
        """Ensures critical base variables are set."""
        if not cls.BASE_URL:
            raise EnvironmentError("CRITICAL: BASE_URL is not defined.")