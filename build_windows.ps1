$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$sourceCommit = & git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw "Release build requires a Git checkout with a readable HEAD." }
$sourceCommit = $sourceCommit.Trim()
$worktreeChanges = & git status --porcelain
if ($LASTEXITCODE -ne 0) { throw "Could not inspect Git working-tree status." }
if ($worktreeChanges) {
    Write-Host "Working-tree changes detected:"
    $worktreeChanges | ForEach-Object { Write-Host "  $_" }
    throw "Release build requires a clean working tree, including no untracked non-ignored files."
}
Write-Host "Source commit: $sourceCommit"
Write-Host "Working tree: clean"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python Launcher for Windows is required for the release build." }
$selected = $null
foreach ($version in @("3.13", "3.12", "3.11", "3.10")) {
    & py "-$version" -c "import struct, sys; sys.exit(0 if struct.calcsize('P') * 8 == 64 else 1)" *> $null
    if ($LASTEXITCODE -eq 0) {
        $selected = $version
        break
    }
}
if (-not $selected) { throw "Python 3.10-3.13 x64 is required for the release build. Python 3.12 or 3.13 is recommended." }

$workspace = Join-Path ([System.IO.Path]::GetTempPath()) ("faithful-markdown-release-" + [guid]::NewGuid().ToString("N"))
$venv = Join-Path $workspace "venv"
$workPath = Join-Path $workspace "pyinstaller-work"
$specPath = Join-Path $workspace "pyinstaller-spec"
$distPath = Join-Path $PSScriptRoot "dist"
$exe = Join-Path $distPath "Markdown_Reader_Editor.exe"
$assetPath = Join-Path $PSScriptRoot "assets\index.html"

New-Item -ItemType Directory -Path $workspace, $workPath, $specPath | Out-Null
try {
    Write-Host "Temporary build workspace: $workspace"
    Write-Host "Creating fresh build environment with Python $selected..."
    & py "-$selected" -m venv $venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create the fresh release virtual environment." }

    $python = Join-Path $venv "Scripts\python.exe"
    $pythonFull = & $python -c "import sys; print(sys.version.replace('\n', ' '))"
    $bits = & $python -c "import struct; print(struct.calcsize('P') * 8)"
    Write-Host "Python: $pythonFull"
    Write-Host "Architecture: $bits-bit"
    Write-Host "pip: $(& $python -m pip --version)"

    & $python -m pip install -r requirements-build.txt
    if ($LASTEXITCODE -ne 0) { throw "Build dependency installation failed." }

    & $python -c "import importlib.metadata as m; print('pywebview:', m.version('pywebview')); print('mistune:', m.version('mistune')); print('PyInstaller:', m.version('pyinstaller'))"
    if ($LASTEXITCODE -ne 0) { throw "Could not report installed release package versions." }
    Write-Host "Installed packages (pip freeze):"
    & $python -m pip freeze
    if ($LASTEXITCODE -ne 0) { throw "Could not report the installed package set." }

    Write-Host "Running full unit tests: python -m unittest discover -s tests -v"
    & $python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Unit tests failed." }

    Write-Host "PyInstaller work path: $workPath"
    Write-Host "PyInstaller spec path: $specPath"
    Write-Host "PyInstaller dist path: $distPath"
    Write-Host "PyInstaller command: `"$python`" -m PyInstaller --noconfirm --clean --onefile --windowed --name Markdown_Reader_Editor --add-data `"$assetPath;assets`" --workpath `"$workPath`" --specpath `"$specPath`" --distpath `"$distPath`" app.py"

    if (Test-Path $exe) { Remove-Item $exe -ErrorAction Stop }

    & $python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name "Markdown_Reader_Editor" `
        --add-data "$assetPath;assets" `
        --workpath $workPath `
        --specpath $specPath `
        --distpath $distPath `
        app.py
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller release build failed." }
    if (-not (Test-Path $exe)) { throw "Build failed: $exe was not created." }

    $exeInfo = Get-Item $exe
    $exeHash = Get-FileHash $exe -Algorithm SHA256
    Write-Host ""
    Write-Host "Build complete: $($exeInfo.FullName)"
    Write-Host "EXE size (bytes): $($exeInfo.Length)"
    Write-Host "EXE SHA-256: $($exeHash.Hash)"
}
finally {
    if (Test-Path $workspace) {
        try {
            Remove-Item $workspace -Recurse -ErrorAction Stop
        }
        catch {
            Write-Warning "Could not clean temporary workspace '$workspace': $($_.Exception.Message)"
        }
    }
}
