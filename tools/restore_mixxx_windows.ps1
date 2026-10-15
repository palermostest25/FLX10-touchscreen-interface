[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$BackupPath)
$ErrorActionPreference = 'Stop'
if (Get-Process -Name mixxx -ErrorAction SilentlyContinue) { throw 'Close Mixxx before restoring.' }
$BackupPath = [IO.Path]::GetFullPath($BackupPath)
$manifest = Get-Content (Join-Path $BackupPath 'install-manifest.json') -Raw | ConvertFrom-Json
$homePath = [IO.Path]::GetFullPath($manifest.mixxxHome)
$allowed = @('mixxx.cfg','skins/AZ Touch','controllers/AZ-Touch-FLX10-scripts.js','controllers/AZ-Touch-FLX10.midi.xml')
foreach ($item in $manifest.targets) {
    if ($item.path -notin $allowed) { throw "Unexpected backup target: $($item.path)" }
    if ($item.existed -and !(Test-Path (Join-Path $BackupPath $item.path))) { throw "Incomplete backup: $($item.path)" }
}
foreach ($item in $manifest.targets) {
    $target = Join-Path $homePath $item.path
    if (Test-Path $target) { Remove-Item -LiteralPath $target -Recurse -Force }
    if ($item.existed) {
        New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $BackupPath $item.path) -Destination $target -Recurse -Force
    }
}
Write-Host "Restored AZ Touch installation targets from $BackupPath"
