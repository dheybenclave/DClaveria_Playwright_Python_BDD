import json
import json
import random
import string
from pathlib import Path


class Utility:
    def __init__(self):
        self.base_data_path = Path(__file__).resolve().parents[1] / "tests" / "test_datas"

    def get_json_data(self, filename, id=None):
        file_path = self.base_data_path / "json" / filename

        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found at: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if id:
            return next((item for item in data if item["id"] == str(id)), None)
        return data

    @staticmethod
    def random_string(length=8):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))
