[int]$newBrightness=-15
# Get current display brightness using WMI
$currentBrightness = (Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness)

# Extract the current brightness value
$currentBrightnessValue = $currentBrightness.CurrentBrightness

# Print the current brightness value
Write-Host "Current Display Brightness: $currentBrightnessValue"

# Calculate the new brightness value by adding the adjustment
$newBrightnessValue = [math]::max(0, [math]::min(100, $currentBrightnessValue + $newBrightness))

Write-Host "New Display Brightness: $newBrightnessValue"

# Adjust display brightness using WMI
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, $newBrightnessValue)
