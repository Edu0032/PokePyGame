param(
    [string]$ApiUrl = "https://pokepygame.onrender.com",
    [switch]$Fallback,
    [switch]$Console
)

$ErrorActionPreference = "Stop"
$arguments = @(
    "scripts/build_executable.py",
    "--api-url", $ApiUrl,
    "--onedir"
)
if ($Fallback) { $arguments += "--fallback" }
if ($Console) { $arguments += "--console" }
python @arguments
