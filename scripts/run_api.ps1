$env:POKEPY_API_HOST="0.0.0.0"
$env:POKEPY_API_PORT="8000"
uvicorn PokePY.api.main:app --host 0.0.0.0 --port 8000 --reload
