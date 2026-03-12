# tests/utils/context.py
import json
import logging
import os


class TestContext:
    def __init__(self):
        self.directory = os.path.join("test-results", "test_state")
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            os.makedirs(self.directory, exist_ok=True)
        except (PermissionError, FileExistsError):
            pass

        self.pid = os.getpid()
        self.filepath = os.path.join(self.directory, f"e2e_data_worker_{self.pid}.json")
        self.data = {}

    def set(self, key, value):
        self.data[key] = value
        self._write_file()

    def get_strict(self, key):
        self._read_file()
        if key not in self.data:
            raise KeyError(
                f"Key '{key}' not found for Worker {self.pid} in {self.filepath}. "
                "Check if the previous sequence step failed."
            )
        return self.data[key]

    def _write_file(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except PermissionError:
            self.logger.warning("Unable to write test state file: %s", self.filepath)

    def _read_file(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.data = json.load(f)
            except PermissionError:
                self.logger.warning("Unable to read test state file: %s", self.filepath)

    def cleanup(self):
        if os.path.exists(self.filepath):
            try:
                os.remove(self.filepath)
            except PermissionError:
                self.logger.warning("Unable to delete test state file: %s", self.filepath)


context = TestContext()
