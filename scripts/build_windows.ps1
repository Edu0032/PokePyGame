param(
  [string]$ApiUrl = "http://127.0.0.1:8000"
)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt
python scripts/build_executable.py --api-url $ApiUrl
