# Registers the daily 5:01 PM IST trigger in Windows Task Scheduler
# Silent execution in background with logging to logs/daily_trigger.log

$TaskName = "AntiGravity_Stock_Screener_Daily_5PM"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunnerScript = Join-Path $ScriptDir "run_daily_trigger.ps1"

# Action: Run PowerShell completely hidden without console pop-up
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$RunnerScript`"" `
    -WorkingDirectory $ScriptDir

# Trigger: Monday to Friday at 5:01 PM IST
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At 5:01PM

# Settings: Wake from sleep, run even on battery, catch up if missed
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Triggers AntiGravity Stock Screener GitHub Action silently at 5:01 PM IST every trading day" `
    -Force | Out-Null

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "✅ Solution 1 is FULLY CONFIGURED & ACTIVE!" -ForegroundColor Green
Write-Host "Task Name : $TaskName"
Write-Host "Schedule  : Mon - Fri at 5:01 PM IST"
Write-Host "Action    : Triggers GitHub Action via gh CLI (Zero queue delay)"
Write-Host "Features  : Silent background run, Wake-on-sleep, Battery-safe, Catch-up enabled"
Write-Host "Log file  : $ScriptDir\logs\daily_trigger.log"
Write-Host "=================================================================" -ForegroundColor Cyan
