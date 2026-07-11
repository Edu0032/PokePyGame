param([string]$ApiUrl = "https://pokepygame.onrender.com")
$env:POKEPY_API_BASE_URL = $ApiUrl
$env:POKEPY_BACKEND_MODE = "api"
$env:POKEPY_LEADERBOARD_BACKEND = "api"
$env:POKEPY_PROGRESS_BACKEND = "api"
$env:POKEPY_MULTIPLAYER_BACKEND = "api"
python -m PokePY.main
