# Changelog

## 4.0.0 - Portfolio Distribution Release

### Added

- Render Blueprint for hosted FastAPI deployment.
- PostgreSQL support for cloud deployment while preserving MySQL for local Docker.
- PyInstaller build workflow for executable distribution.
- Runtime client configuration through `pokepy_client.json`.
- User data directory handling for frozen executable builds.
- API readiness endpoint at `/health/ready`.
- Source setup guide.
- Render deployment guide.
- Executable distribution guide.
- Evaluator guide.
- Asset usage documentation.
- Portfolio release checklist.
- Fallback repository for remote player progress.
- Windows and Linux/macOS helper scripts for setup, tests, local play, online play and packaging.

### Changed

- Client backend configuration now supports independent leaderboard, progress and multiplayer backends.
- API settings include production-oriented table creation control through `POKEPY_AUTO_CREATE_TABLES`.
- Database URL normalization supports PostgreSQL URLs used by cloud providers.
- README now presents source execution and executable distribution as separate workflows.

## 3.0.0 - Professional Architecture Release

### Added

- State Machine structure for the Pygame client.
- Professional documentation set.
- Pytest configuration.
- GitHub Actions, pre-commit and repository health files.
- Alembic migration structure.
