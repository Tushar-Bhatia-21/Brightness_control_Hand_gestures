$wshShell = New-Object -ComObject WScript.Shell
$audioLevel = 1  # Number of times to press the volume up key

1..$audioLevel | ForEach-Object {
    $wshShell.SendKeys([char]173)
    Start-Sleep -Milliseconds 100  # Adjust sleep time if needed
}
#173=mute
#175=increase
#174=decrease
