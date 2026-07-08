param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $ProjectRoot

& "$ProjectRoot\.venv\Scripts\python.exe" -m uvicorn app.main:app --host $HostAddress --port $Port
