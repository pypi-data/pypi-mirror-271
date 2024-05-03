from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ApiCallResponse:
    status_code: int
    successful: bool
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict = field(default_factory=dict)

    def get_json_value(self, key: str):
        if self.body is None:
            return None

        try:
            return self.body[key]
        except KeyError:
            return None
