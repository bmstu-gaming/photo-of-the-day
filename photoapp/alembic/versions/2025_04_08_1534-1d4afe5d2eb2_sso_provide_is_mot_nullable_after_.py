"""sso_provide is mot nullable after migration

Revision ID: 1d4afe5d2eb2
Revises: aa7e2f69b0bd
Create Date: 2025-04-08 15:34:25.713590

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1d4afe5d2eb2"
down_revision: Union[str, None] = "aa7e2f69b0bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users", "sso_provider", existing_type=sa.VARCHAR(), nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users", "sso_provider", existing_type=sa.VARCHAR(), nullable=True
    )
