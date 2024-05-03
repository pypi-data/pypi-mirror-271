from typing import Dict, List

Primitive = str | int | float | bool | None
JsonData = Dict[str, Primitive | List | Dict]
