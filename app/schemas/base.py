import datetime

from pydantic import BaseModel as PBaseModel, ConfigDict
from pydantic.utils import to_camel


def to_lower_camel(string: str) -> str:
    s = to_camel(string)

    return s[0].lower() + s[1:]


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class BaseModel(PBaseModel):
    model_config = ConfigDict(alias_generator=to_lower_camel, populate_by_name=True)
