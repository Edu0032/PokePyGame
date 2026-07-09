from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260702_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leaderboard_scores",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("player_name", sa.String(length=80), nullable=False),
        sa.Column("elapsed_seconds", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_leaderboard_scores_player_name", "leaderboard_scores", ["player_name"])
    op.create_index("ix_leaderboard_scores_elapsed_seconds", "leaderboard_scores", ["elapsed_seconds"])
    op.create_index("ix_leaderboard_scores_created_at", "leaderboard_scores", ["created_at"])
    op.create_table(
        "player_progress",
        sa.Column("player_id", sa.String(length=80), nullable=False),
        sa.Column("player_name", sa.String(length=80), nullable=False),
        sa.Column("zone_index", sa.Integer(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("items", sa.JSON(), nullable=False),
        sa.Column("team", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("player_id"),
    )
    op.create_table(
        "multiplayer_tickets",
        sa.Column("ticket_id", sa.String(length=80), nullable=False),
        sa.Column("player_id", sa.String(length=80), nullable=False),
        sa.Column("player_snapshot", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("match_id", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("ticket_id"),
    )
    op.create_index("ix_multiplayer_tickets_player_id", "multiplayer_tickets", ["player_id"])
    op.create_index("ix_multiplayer_tickets_status", "multiplayer_tickets", ["status"])
    op.create_index("ix_multiplayer_tickets_match_id", "multiplayer_tickets", ["match_id"])
    op.create_table(
        "multiplayer_matches",
        sa.Column("match_id", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("players", sa.JSON(), nullable=False),
        sa.Column("active_player_id", sa.String(length=80), nullable=True),
        sa.Column("winner_player_id", sa.String(length=80), nullable=True),
        sa.Column("turn_number", sa.Integer(), nullable=False),
        sa.Column("events", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("match_id"),
    )
    op.create_index("ix_multiplayer_matches_status", "multiplayer_matches", ["status"])
    op.create_index("ix_multiplayer_matches_active_player_id", "multiplayer_matches", ["active_player_id"])
    op.create_index("ix_multiplayer_matches_winner_player_id", "multiplayer_matches", ["winner_player_id"])
    op.create_table(
        "multiplayer_actions",
        sa.Column("action_id", sa.String(length=80), nullable=False),
        sa.Column("match_id", sa.String(length=80), nullable=False),
        sa.Column("player_id", sa.String(length=80), nullable=False),
        sa.Column("action_type", sa.String(length=40), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("action_id"),
    )
    op.create_index("ix_multiplayer_actions_match_id", "multiplayer_actions", ["match_id"])
    op.create_index("ix_multiplayer_actions_player_id", "multiplayer_actions", ["player_id"])


def downgrade() -> None:
    op.drop_index("ix_multiplayer_actions_player_id", table_name="multiplayer_actions")
    op.drop_index("ix_multiplayer_actions_match_id", table_name="multiplayer_actions")
    op.drop_table("multiplayer_actions")
    op.drop_index("ix_multiplayer_matches_winner_player_id", table_name="multiplayer_matches")
    op.drop_index("ix_multiplayer_matches_active_player_id", table_name="multiplayer_matches")
    op.drop_index("ix_multiplayer_matches_status", table_name="multiplayer_matches")
    op.drop_table("multiplayer_matches")
    op.drop_index("ix_multiplayer_tickets_match_id", table_name="multiplayer_tickets")
    op.drop_index("ix_multiplayer_tickets_status", table_name="multiplayer_tickets")
    op.drop_index("ix_multiplayer_tickets_player_id", table_name="multiplayer_tickets")
    op.drop_table("multiplayer_tickets")
    op.drop_table("player_progress")
    op.drop_index("ix_leaderboard_scores_created_at", table_name="leaderboard_scores")
    op.drop_index("ix_leaderboard_scores_elapsed_seconds", table_name="leaderboard_scores")
    op.drop_index("ix_leaderboard_scores_player_name", table_name="leaderboard_scores")
    op.drop_table("leaderboard_scores")
