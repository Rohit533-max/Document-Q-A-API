"""Initial database schema

Revision ID: 20261127_1933
Revises:
Create Date: 2026-11-27 19:33:43
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261127_1933"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "user_table" not in existing_tables:
        op.create_table(
            "user_table",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(), nullable=True),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )
    if "ix_user_table_id" not in {
        index["name"] for index in inspector.get_indexes("user_table")
    }:
        op.create_index(
            op.f("ix_user_table_id"), "user_table", ["id"], unique=False
        )

    if "document_table" not in existing_tables:
        op.create_table(
            "document_table",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            ),
            sa.Column("owner_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["owner_id"], ["user_table.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
    if "ix_document_table_id" not in {
        index["name"] for index in inspector.get_indexes("document_table")
    }:
        op.create_index(
            op.f("ix_document_table_id"), "document_table", ["id"], unique=False
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_document_table_id"), table_name="document_table")
    op.drop_table("document_table")
    op.drop_index(op.f("ix_user_table_id"), table_name="user_table")
    op.drop_table("user_table")
