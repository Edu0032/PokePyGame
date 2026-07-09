param(
  [string]$ApiUrl = "http://127.0.0.1:8000"
)

$env:POKEPY_BACKEND_MODE="api"
$env:POKEPY_LEADERBOARD_BACKEND="api"
$env:POKEPY_PROGRESS_BACKEND="api"
$env:POKEPY_API_BASE_URL=$ApiUrl
python -m PokePY.main
