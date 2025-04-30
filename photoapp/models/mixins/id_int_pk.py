from sqlalchemy.orm import Mapped, mapped_column


# Id is present in all tables, so we mix it in
class IdIntPKMixin:
    id: Mapped[int] = mapped_column(primary_key=True)