from typing import Dict

from pydantic import BaseModel


class HttpCallResponse(BaseModel):
    status_code: int
    json_data: Dict | None = None

    def get_json_value(self, key: str):
        if self.json_data is None:
            return None

        try:
            return self.json_data[key]
        except KeyError:
            return None
