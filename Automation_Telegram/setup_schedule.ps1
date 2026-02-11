$taskName = "MeBaVi_Daily_Telegram"
$actionPath = "C:\Users\USER\.gemini\antigravity\scratch\NotebookLM\Automation_Telegram\run_daily.bat"
$triggerTime = "08:00"

# Create Action
$action = New-ScheduledTaskAction -Execute $actionPath

# Create Trigger (Daily at 8:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime

# Register Task
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $taskName -Description "Gui bai thuoc Me Ba Vi hang ngay qua Telegram" -Force

Write-Host "Task '$taskName' has been scheduled daily at $triggerTime."
