from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: int
