from pydantic import BaseModel
from pydantic.utils import to_camel


def to_lower_camel(string: str) -> str:
    s = to_camel(string)

    return s[0].lower() + s[1:]


class BaseModel(BaseModel):
    class Config:
        alias_generator = to_lower_camel
