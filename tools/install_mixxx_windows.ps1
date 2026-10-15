[CmdletBinding()]
param(
    [string]$MixxxHome = (Join-Path $env:LOCALAPPDATA 'Mixxx'),
    [switch]$IncludeController
)
$ErrorActionPreference = 'Stop'
if (Get-Process -Name mixxx -ErrorAction SilentlyContinue) { throw 'Close Mixxx before installing.' }
$project = Split-Path $PSScriptRoot -Parent
$skin = Join-Path $project 'mixxx/AZ Touch'
if (!(Test-Path (Join-Path $skin 'skin.xml'))) { throw 'Extract the entire project ZIP first.' }
$MixxxHome = [IO.Path]::GetFullPath($MixxxHome)
$stage = Join-Path ([IO.Path]::GetTempPath()) ('AZTouch-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -Force | Out-Null

function Set-MixxxSetting([string]$Text, [string]$Section, [string]$Key, [string]$Value) {
    $lines = [Collections.Generic.List[string]]::new()
    foreach ($line in ($Text -split '\r?\n')) { $lines.Add($line) }
    $heading = "[$Section]"
    $start = $lines.IndexOf($heading)
    if ($start -lt 0) { $lines.Add($heading); $lines.Add("$Key $Value"); return ($lines -join "`r`n") }
    $end = $start + 1
    while ($end -lt $lines.Count -and $lines[$end] -notmatch '^\[') { $end++ }
    for ($i = $start + 1; $i -lt $end; $i++) {
        if ($lines[$i] -match ('^' + [regex]::Escape($Key) + '\s')) {
            $lines[$i] = "$Key $Value"; return ($lines -join "`r`n")
        }
    }
    $lines.Insert($end, "$Key $Value")
    return ($lines -join "`r`n")
}

try {
    $targets = @('mixxx.cfg', 'skins/AZ Touch')
    if ($IncludeController) {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $lock = Get-Content (Join-Path $project 'mixxx/controller-sources.lock.json') -Raw | ConvertFrom-Json
        foreach ($file in $lock.files) {
            $download = Join-Path $stage $file.destination
            Invoke-WebRequest -Uri $file.url -OutFile $download -UseBasicParsing
            if ((Get-FileHash $download -Algorithm SHA256).Hash -ne $file.sha256) { throw "Hash mismatch: $($file.destination)" }
            $targets += ('controllers/' + $file.destination)
        }
        $xmlPath = Join-Path $stage 'AZ-Touch-FLX10.midi.xml'
        [xml]$mapping = Get-Content $xmlPath -Raw
        $mapping.MixxxControllerPreset.info.name = 'AZ Touch FLX10 - MIDI only'
        $mapping.MixxxControllerPreset.controller.scriptfiles.file.filename = 'AZ-Touch-FLX10-scripts.js'
        $mapping.Save($xmlPath)
    }
    $backup = Join-Path $MixxxHome ('AZTouch-backups/' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
    New-Item -ItemType Directory -Path $backup -Force | Out-Null
    $manifest = @()
    foreach ($relative in $targets) {
        $target = Join-Path $MixxxHome $relative
        $exists = Test-Path $target
        $manifest += [pscustomobject]@{ path = $relative; existed = $exists }
        if ($exists) {
            $saved = Join-Path $backup $relative
            New-Item -ItemType Directory -Path (Split-Path $saved -Parent) -Force | Out-Null
            Copy-Item -LiteralPath $target -Destination $saved -Recurse -Force
        }
    }
    [pscustomobject]@{ mixxxHome = $MixxxHome; targets = $manifest } | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $backup 'install-manifest.json') -Encoding UTF8
    Write-Host "Backup: $backup"
    try {
        $destination = Join-Path $MixxxHome 'skins/AZ Touch'
        New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
        if (Test-Path $destination) { Remove-Item -LiteralPath $destination -Recurse -Force }
        Copy-Item -LiteralPath $skin -Destination $destination -Recurse
        if ($IncludeController) {
            New-Item -ItemType Directory -Path (Join-Path $MixxxHome 'controllers') -Force | Out-Null
            foreach ($file in $lock.files) { Copy-Item (Join-Path $stage $file.destination) (Join-Path $MixxxHome ('controllers/' + $file.destination)) -Force }
        }
        $cfgPath = Join-Path $MixxxHome 'mixxx.cfg'
        $cfg = if (Test-Path $cfgPath) { [IO.File]::ReadAllText($cfgPath) } else { '' }
        foreach ($setting in @(
            @('Config','ResizableSkin','AZ Touch'),
            @('Waveform','WaveformType','19'),
            @('Waveform','WaveformOverviewType','0'),
            @('Waveform','FrameRate','30'),
            @('Waveform','beatGridAlpha','80'),
            @('Controls','AllowTrackLoadToPlayingDeck','0'),
            @('Controls','LoadWhenDeckPlaying','0'),
            @('Controls','ShowDurationRemaining','1')
        )) { $cfg = Set-MixxxSetting $cfg $setting[0] $setting[1] $setting[2] }
        [IO.File]::WriteAllText($cfgPath, $cfg, [Text.UTF8Encoding]::new($false))
    } catch {
        & (Join-Path $PSScriptRoot 'restore_mixxx_windows.ps1') -BackupPath $backup
        throw
    }
    Write-Host 'Installed AZ Touch. Audio routing is unchanged. Start Mixxx and configure Sound Hardware.'
    if ($IncludeController) { Write-Host 'Select AZ Touch FLX10 - MIDI only in Preferences > Controllers; enable it on the FLX10 MIDI input.' }
    Write-Host "Rollback: .\tools\restore_mixxx_windows.ps1 -BackupPath `"$backup`""
} finally {
    if (Test-Path $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}
