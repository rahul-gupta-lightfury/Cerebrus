param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$LogFile = "$env:TEMP\cerebrus_install_debug.txt"

function Write-Log($message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMsg = "[$timestamp] [DependencyInstaller] $message"
    Write-Host $logMsg -ForegroundColor Cyan
    Add-Content -Path $LogFile -Value $logMsg
}

Write-Log "Starting dependency check..."
Write-Log "Running as user: $env:USERNAME"


function Ensure-WingetAvailable {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Log "winget is required to install dependencies. Please install App Installer from Microsoft Store."
        exit 1
    }
}

function Ensure-Python {
    Write-Log "Checking Python..."
    $python = Get-Command py -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command python -ErrorAction SilentlyContinue
    }

    if ($python) {
        $version = & $python.Source -c "import sys; print('{}.{}'.format(*sys.version_info[:2]))" 2>$null
        if ($version -and [version]$version -ge [version]"3.11") {
            Write-Log "Found Python $version"
            return
        }
        Write-Log "Python found but below 3.11."
    }
    else {
        Write-Log "Python not found."
    }

    Write-Log "Installing Python 3.11 via winget..."
    Ensure-WingetAvailable
    winget install --id Python.Python.3.11 --exact --silent --accept-package-agreements --accept-source-agreements --force
}

function Ensure-Adb {
    Write-Log "Checking ADB..."
    if (Get-Command adb -ErrorAction SilentlyContinue) {
        Write-Log "ADB found."
        return
    }

    Write-Log "ADB not found. Installing Google Android SDK Platform Tools via winget..."
    Ensure-WingetAvailable
    winget install --id Google.AndroidSDK.PlatformTools --exact --silent --accept-package-agreements --accept-source-agreements --force
}

try {
    Ensure-Python
    Ensure-Adb
    Write-Log "Dependencies check complete."
    exit 0
}
catch {
    Write-Error $_
    exit 1
}
