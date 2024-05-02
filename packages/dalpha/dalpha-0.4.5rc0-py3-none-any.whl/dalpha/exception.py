from enum import Enum
from typing import Dict


class WaitException(Exception):
    def __init__(self, message: str = "Wait Exception occurred"):
        super().__init__(message)


class ExpectedError(Exception):
    def __init__(self, error_json: Dict, message: str = "Expected Error occured"):
        super().__init__(message)
        self.error_json = error_json


class BaseStatusCode(Enum):
    BAD_REQUEST = 400
    CONFLICT = 409
    INTERNAL_ERROR = 525

    def __str__(self):
        return f"({self.value})"
