"""Add image URL columns to artists, albums, and users

Revision ID: add_image_urls
Revises: 91d94beea65e
Create Date: 2026-05-01 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_image_urls"
down_revision: Union[str, None] = "91d94beea65e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("artists", sa.Column("photo_url", sa.String(), nullable=True))
    op.add_column("albums", sa.Column("cover_image_url", sa.String(), nullable=True))
    op.add_column("users", sa.Column("avatar_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
    op.drop_column("albums", "cover_image_url")
    op.drop_column("artists", "photo_url")
