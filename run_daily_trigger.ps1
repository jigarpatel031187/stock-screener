# Daily trigger runner for AntiGravity Stock Screener
# Executed silently by Windows Task Scheduler every trading day at 5:01 PM IST

$WorkingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $WorkingDir "logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}
$LogFile = Join-Path $LogDir "daily_trigger.log"
$Timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

Add-Content -Path $LogFile -Value "[$Timestamp] Triggering AntiGravity Stock Screener GitHub Action..."

try {
    $GhPath = (Get-Command gh -ErrorAction SilentlyContinue).Source
    if (-not $GhPath) {
        $GhPath = "C:\Program Files\GitHub CLI\gh.exe"
    }
    
    $output = & $GhPath workflow run nifty_momentum_alert.yml -R jigarpatel031187/stock-screener 2>&1
    Add-Content -Path $LogFile -Value "[$Timestamp] SUCCESS: Dispatch sent to GitHub Actions! ($output)"
} catch {
    Add-Content -Path $LogFile -Value "[$Timestamp] ERROR: Failed to trigger workflow: $_"
}
