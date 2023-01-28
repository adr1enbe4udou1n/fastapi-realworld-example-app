from typing import Any

from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: Any
