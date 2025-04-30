from inflection import underscore

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config.settings import settings


class ModelBase(DeclarativeBase):
    __abstract__ = True

    # Setup naming convention - Alembic wont generate names if we do not do it
    metadata = MetaData(
        naming_convention=settings.db.naming_conventions
    )

    # Automatically generate tablenames in snake case from CamelCase model class names with s at the end
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{underscore(cls.__name__)}s"
