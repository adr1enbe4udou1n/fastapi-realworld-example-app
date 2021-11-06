import datetime

from pydantic import BaseModel as PBaseModel
from pydantic.main import BaseConfig
from pydantic.utils import to_camel


def to_lower_camel(string: str) -> str:
    s = to_camel(string)

    return s[0].lower() + s[1:]


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class BaseModel(PBaseModel):
    class Config(BaseConfig):
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
