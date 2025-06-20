"""2 migration

Revision ID: 4d9b3f2caa9b
Revises:
Create Date: 2025-06-13 20:07:50.448525

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d9b3f2caa9b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "manipulation_facts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pet_id", sa.Integer(), nullable=False),
        sa.Column("manipulation_id", sa.Integer(), nullable=False),
        sa.Column("is_planned", sa.Boolean(), nullable=True),
        sa.Column("begin_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "manipulations",
        sa.Column(
            "manipulation_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("manipulation_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("manipulation_id"),
    )
    op.create_table(
        "owners",
        sa.Column(
            "owner_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("owner_name", sa.String(), nullable=False),
        sa.Column("owner_phone", sa.String(), nullable=True),
        sa.Column("owner_email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("owner_id"),
    )
    op.create_table(
        "pets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("species", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("sex", sa.String(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("birthdate", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "species",
        sa.Column(
            "species_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("species_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("species_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("species")
    op.drop_table("pets")
    op.drop_table("owners")
    op.drop_table("manipulations")
    op.drop_table("manipulation_facts")
    # ### end Alembic commands ###
