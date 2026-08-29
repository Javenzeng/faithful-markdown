$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    $selected = $null
    foreach ($version in @("3.13", "3.12", "3.11", "3.10")) {
        & py "-$version" -c "import sys; print(sys.version)" *> $null
        if ($LASTEXITCODE -eq 0) {
            $selected = $version
            break
        }
    }
    if (-not $selected) {
        throw "Python 3.10-3.13 x64 is required for the release build. Python 3.12 or 3.13 is recommended."
    }
    Write-Host "Creating build environment with Python $selected..."
    & py "-$selected" -m venv .venv
}

$python = ".\.venv\Scripts\python.exe"
$versionInfo = & $python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$bits = & $python -c "import struct; print(struct.calcsize('P') * 8)"

if ($bits -ne "64") {
    throw "Final Windows build must use 64-bit Python. Current interpreter: $bits-bit."
}
if ([version]$versionInfo -lt [version]"3.10" -or [version]$versionInfo -ge [version]"3.14") {
    throw "Release build requires Python 3.10-3.13. Current .venv uses Python $versionInfo. Delete .venv and rerun this script."
}

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements-build.txt
& $python -m unittest discover -s tests -v

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "Markdown_Reader_Editor" `
    --add-data "assets/index.html;assets" `
    app.py

$exe = "dist\Markdown_Reader_Editor.exe"
if (-not (Test-Path $exe)) {
    throw "Build failed: $exe was not created."
}

Write-Host ""
Write-Host "Build complete: $exe"
Get-FileHash $exe -Algorithm SHA256
