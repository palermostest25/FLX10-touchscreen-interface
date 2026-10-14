# Select your previous/default skin in VirtualDJ, then close VirtualDJ first.
[CmdletBinding(SupportsShouldProcess)]
param([Parameter(Mandatory)] [string] $ReceiptPath)
. (Join-Path $PSScriptRoot 'windows_common.ps1')
Assert-VirtualDJClosed
$receiptFile = (Resolve-Path -LiteralPath $ReceiptPath).Path
$r = Get-Content -LiteralPath $receiptFile -Raw | ConvertFrom-Json
if ($r.Schema -ne 1) { throw 'Unsupported rollback receipt.' }
$vdjPath = Resolve-VirtualDJHome $r.VirtualDJHome
$name = Split-Path -Leaf $r.Destination
if ($name -notin @('AZ-Touch-3x2.zip','AZ-Touch-SDK-Spike.zip')) { throw 'Receipt points at an unexpected skin.' }
$destination = Join-Path (Join-Path $vdjPath 'Skins') $name
if ([IO.Path]::GetFullPath($destination) -ne [IO.Path]::GetFullPath($r.Destination)) { throw 'Receipt destination does not match the VirtualDJ Skins folder.' }
if (-not (Test-Path -LiteralPath $destination)) { throw 'Skin is already absent. No files changed.' }
if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.InstalledHash) {
    throw 'The installed skin has changed since this receipt. Refusing to remove it; use the matching receipt.'
}
if ($r.PreviousPackage) {
    $expectedBackup = Join-Path (Split-Path -Parent $receiptFile) $name
    if ([IO.Path]::GetFullPath($r.PreviousPackage) -ne [IO.Path]::GetFullPath($expectedBackup)) { throw 'Backup path is outside the receipt directory.' }
    if ((Get-FileHash -LiteralPath $expectedBackup -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.PreviousHash) { throw 'Previous package backup checksum mismatch.' }
}
if (-not $PSCmdlet.ShouldProcess($destination, 'Remove installed AZ Touch or restore its backed-up package')) { return }
if ($r.PreviousPackage) {
    Copy-Item -LiteralPath $r.PreviousPackage -Destination $destination -Force
    Write-Output "Restored previous package: $destination"
} else {
    Remove-Item -LiteralPath $destination
    Write-Output "Removed AZ Touch: $destination"
}
Write-Output 'Settings, mappings, playlists, and databases were not changed. Open VirtualDJ and select your previous/default skin.'
