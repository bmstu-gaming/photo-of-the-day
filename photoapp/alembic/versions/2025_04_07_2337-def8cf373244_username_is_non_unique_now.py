"""Username is non unique now

Revision ID: def8cf373244
Revises: 9d1f9084f603
Create Date: 2025-04-07 23:37:18.598380

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "def8cf373244"
down_revision: Union[str, None] = "9d1f9084f603"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("uq_users_username", "users", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint("uq_users_username", "users", ["username"])
