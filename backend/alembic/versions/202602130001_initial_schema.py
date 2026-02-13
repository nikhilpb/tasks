"""Initial schema baseline for Family Task Manager.

Revision ID: 202602130001
Revises:
Create Date: 2026-02-13 00:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202602130001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("google_sub", sa.String(length=255), nullable=False, unique=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deadline_date", sa.Date(), nullable=True),
        sa.Column("priority", sa.String(length=2), nullable=False, server_default="P2"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="todo"),
        sa.Column("assignee_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("parent_task_id", sa.String(length=36), sa.ForeignKey("tasks.id"), nullable=True),
        sa.Column("created_by", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_index("ix_tasks_assignee_id", "tasks", ["assignee_id"])
    op.create_index("ix_tasks_deadline_date", "tasks", ["deadline_date"])
    op.create_index("ix_tasks_priority", "tasks", ["priority"])
    op.create_index("ix_tasks_status", "tasks", ["status"])

    op.create_table(
        "task_dependencies",
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
        sa.Column(
            "blocked_by_task_id",
            sa.String(length=36),
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("created_by", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("name", "created_by", name="uq_tags_name_created_by"),
    )

    op.create_table(
        "task_tags",
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.String(length=36), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "calendar_sync",
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("google_event_id", sa.String(length=255), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sync_status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("sync_error", sa.Text(), nullable=True),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_notifications_scheduled_for", "notifications", ["scheduled_for"])

    op.create_table(
        "notification_settings",
        sa.Column("family_id", sa.String(length=64), primary_key=True),
        sa.Column("remind_days_before", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("remind_on_due_day", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("overdue_digest_time", sa.String(length=5), nullable=False, server_default="09:00"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("notification_settings")
    op.drop_index("ix_notifications_scheduled_for", table_name="notifications")
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")
    op.drop_table("calendar_sync")
    op.drop_table("task_tags")
    op.drop_table("tags")
    op.drop_table("task_dependencies")
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_priority", table_name="tasks")
    op.drop_index("ix_tasks_deadline_date", table_name="tasks")
    op.drop_index("ix_tasks_assignee_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("users")
