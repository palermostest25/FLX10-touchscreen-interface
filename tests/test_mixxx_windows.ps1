# Runs file operations in isolated fixtures. This does not certify Windows audio/touch.
param([switch]$Network)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$temp = Join-Path ([IO.Path]::GetTempPath()) ('az-mixxx-fixture-' + [guid]::NewGuid().ToString('N'))
$homePath = Join-Path $temp 'Mixxx space'
$savedLocal = $env:LOCALAPPDATA
$checks = 0
function Assert([bool]$ok, [string]$message) { if (!$ok) { throw $message }; $script:checks++ }
try {
    $env:LOCALAPPDATA = $temp
    New-Item -ItemType Directory -Path (Join-Path $homePath 'controllers') -Force | Out-Null
    $cfg = Join-Path $homePath 'mixxx.cfg'
    [IO.File]::WriteAllText($cfg, "[Config]`nResizableSkin LateNight`nKeepMe yes`n[Waveform]`nFrameRate 60`n")
    Set-Content (Join-Path $homePath 'controllers/original.midi.xml') 'keep'
    $hash = (Get-FileHash $cfg).Hash
    & (Join-Path $repo 'tools/install_mixxx_windows.ps1') -MixxxHome $homePath
    $text = Get-Content $cfg -Raw
    Assert ($text -match 'ResizableSkin AZ Touch') 'Skin was not selected'
    Assert ($text -match 'KeepMe yes') 'Existing setting lost'
    Assert ($text -match 'LoadWhenDeckPlaying 0') 'Playing-deck protection missing'
    Assert ($text -match 'WaveformType 19') 'Native three-band renderer missing'
    Assert (Test-Path (Join-Path $homePath 'skins/AZ Touch/LICENSE')) 'GPL missing'
    Assert ((Get-Content (Join-Path $homePath 'controllers/original.midi.xml') -Raw).Trim() -eq 'keep') 'Other mapping changed'
    $backup = (Get-ChildItem (Join-Path $homePath 'AZTouch-backups') -Directory | Select-Object -First 1).FullName
    & (Join-Path $repo 'tools/restore_mixxx_windows.ps1') -BackupPath $backup
    Assert ((Get-FileHash $cfg).Hash -eq $hash) 'Config restore not byte identical'
    Assert (!(Test-Path (Join-Path $homePath 'skins/AZ Touch'))) 'New skin not removed'
    $usb = Join-Path $temp 'USB'
    New-Item -ItemType Directory -Path (Join-Path $usb 'PIONEER/rekordbox') -Force | Out-Null
    Set-Content (Join-Path $usb 'PIONEER/rekordbox/exportLibrary.db') 'test'
    $result = & (Join-Path $repo 'tools/check_rekordbox_usb.ps1') -DriveRoot $usb
    Assert ($result.OneLibrary -and !$result.LegacyDeviceLibrary) 'OneLibrary-only check failed'
    Set-Content (Join-Path $usb 'PIONEER/rekordbox/export.pdb') 'test'
    $result = & (Join-Path $repo 'tools/check_rekordbox_usb.ps1') -DriveRoot $usb
    Assert ($result.OneLibrary -and $result.LegacyDeviceLibrary) 'Dual-library check failed'
    if ($Network) {
        $previousBackup = $backup
        & (Join-Path $repo 'tools/install_mixxx_windows.ps1') -MixxxHome $homePath -IncludeController
        $controller = Join-Path $homePath 'controllers/AZ-Touch-FLX10.midi.xml'
        [xml]$mapping = Get-Content $controller -Raw
        Assert ($mapping.MixxxControllerPreset.info.name -eq 'AZ Touch FLX10 - MIDI only') 'Preset name missing'
        Assert ($mapping.MixxxControllerPreset.controller.scriptfiles.file.filename -eq 'AZ-Touch-FLX10-scripts.js') 'Script reference incorrect'
        $lock = Get-Content (Join-Path $repo 'mixxx/controller-sources.lock.json') -Raw | ConvertFrom-Json
        $js = Join-Path $homePath 'controllers/AZ-Touch-FLX10-scripts.js'
        Assert ((Get-FileHash $js -Algorithm SHA256).Hash -eq $lock.files[0].sha256) 'Downloaded JS hash differs'
        Assert ((Get-ChildItem (Join-Path $homePath 'controllers')).Count -eq 3) 'Unexpected controller files'
        $backup = (Get-ChildItem (Join-Path $homePath 'AZTouch-backups') -Directory | Where-Object { $_.FullName -ne $previousBackup } | Select-Object -First 1).FullName
        & (Join-Path $repo 'tools/restore_mixxx_windows.ps1') -BackupPath $backup
        Assert ((Get-FileHash $cfg).Hash -eq $hash) 'Network install did not restore original config'
        Assert (!(Test-Path $js)) 'Network install mapping not removed'
    }
    Write-Host "PASS: $checks Mixxx file-operation/USB assertions"
} finally {
    $env:LOCALAPPDATA = $savedLocal
    Remove-Item -LiteralPath $temp -Recurse -Force
}
