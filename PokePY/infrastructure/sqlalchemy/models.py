from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from PokePY.infrastructure.sqlalchemy.database import Base


class LeaderboardScoreRecord(Base):
    __tablename__ = "leaderboard_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_name: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    elapsed_seconds: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)


class PlayerProgressRecord(Base):
    __tablename__ = "player_progress"

    player_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    player_name: Mapped[str] = mapped_column(String(80), nullable=False)
    zone_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    x: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    y: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    items: Mapped[dict] = mapped_column(JSON, nullable=False)
    team: Mapped[list] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MultiplayerTicketRecord(Base):
    __tablename__ = "multiplayer_tickets"

    ticket_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    player_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    player_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    match_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MultiplayerMatchRecord(Base):
    __tablename__ = "multiplayer_matches"

    match_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    players: Mapped[list] = mapped_column(JSON, nullable=False)
    active_player_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    winner_player_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    turn_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    events: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MultiplayerActionRecord(Base):
    __tablename__ = "multiplayer_actions"

    action_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    match_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    player_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(40), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
