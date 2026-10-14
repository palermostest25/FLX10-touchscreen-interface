[CmdletBinding(SupportsShouldProcess)]
param([string] $VirtualDJHome)
. (Join-Path $PSScriptRoot 'windows_common.ps1')
Assert-VirtualDJClosed
$vdjPath = Resolve-VirtualDJHome $VirtualDJHome
if (-not $PSCmdlet.ShouldProcess($vdjPath, 'Snapshot local settings, mappings, skins, playlists, and database')) { return }
$backup = New-BackupDirectory $vdjPath
$items = @('settings.xml','database.xml','Mappers','Devices','Skins','Playlists','Folders','History')
# Explicit list: do not traverse music drives, junctions, or other AZ Touch backups.
foreach ($name in $items) {
    $source = Join-Path $vdjPath $name
    if (-not (Test-Path -LiteralPath $source)) { continue }
    $all = @((Get-Item -LiteralPath $source))
    if (Test-Path -LiteralPath $source -PathType Container) {
        $all += @(Get-ChildItem -LiteralPath $source -Recurse -Force)
    }
    if ($all | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }) {
        throw "Found a junction/symlink in $name. Snapshot this item manually; partial backup is at $backup."
    }
    Copy-Item -LiteralPath $source -Destination (Join-Path $backup $name) -Recurse
}
Write-Output "Local snapshot: $backup"
Write-Output 'This does not back up music, external-drive databases, or your rekordbox USB. Clone those separately.'
