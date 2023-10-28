from datetime import UTC, datetime

from pydantic import BaseModel as PBaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


def to_lower_camel(string: str) -> str:
    s = to_camel(string)

    return s[0].lower() + s[1:]


def convert_datetime_to_realworld(dt: datetime) -> str:
    return dt.replace(tzinfo=UTC).isoformat().replace("+00:00", "Z")


class BaseModel(PBaseModel):
    model_config = ConfigDict(alias_generator=to_lower_camel, populate_by_name=True)
