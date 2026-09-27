"""initial

Revision ID: initial_migration
Revises: 
Create Date: 2026-09-27 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "initial_migration"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table("events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("submission_deadline", sa.DateTime(), nullable=True),
        sa.Column("judging_start", sa.DateTime(), nullable=True),
        sa.Column("judging_end", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("organizer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["organizer_id"], ["users.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)
    op.create_index(op.f("ix_events_name"), "events", ["name"], unique=False)

    op.create_table("teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)

    op.create_table("team_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_team_members_id"), "team_members", ["id"], unique=False)

    op.create_table("projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("repository_url", sa.String(), nullable=True),
        sa.Column("demo_url", sa.String(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("submitted_timestamp", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)

    op.create_table("criteria",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("max_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_criteria_id"), "criteria", ["id"], unique=False)

    op.create_table("judge_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ),
        sa.ForeignKeyConstraint(["judge_id"], ["users.id"], ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_judge_assignments_id"), "judge_assignments", ["id"], unique=False)

    op.create_table("scores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("criterion_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["criterion_id"], ["criteria.id"], ),
        sa.ForeignKeyConstraint(["judge_id"], ["users.id"], ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_scores_id"), "scores", ["id"], unique=False)

    op.create_table("results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("weighted_score", sa.Float(), nullable=False),
        sa.Column("normalized_score", sa.Float(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_results_id"), "results", ["id"], unique=False)


def downgrade() -> None:
    pass
