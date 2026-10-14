# Run as your normal Windows user. No administrator privileges required.
[CmdletBinding(SupportsShouldProcess)]
param(
    [string] $VirtualDJHome,
    [string] $SkinZip = (Join-Path $PSScriptRoot '..\dist\AZ-Touch-3x2.zip'),
    [switch] $Replace
)
. (Join-Path $PSScriptRoot 'windows_common.ps1')
Assert-VirtualDJClosed
$vdjPath = Resolve-VirtualDJHome $VirtualDJHome
$packagePath = (Resolve-Path -LiteralPath $SkinZip).Path
$checksumPath = Join-Path (Split-Path -Parent $packagePath) 'SHA256SUMS.txt'
$hash = Assert-Package $packagePath $checksumPath
$destination = Join-Path (Join-Path $vdjPath 'Skins') (Split-Path -Leaf $packagePath)
if ((Test-Path -LiteralPath $destination) -and -not $Replace) {
    throw 'AZ Touch is already present. Use -Replace to back up and replace this skin only.'
}
if (-not $PSCmdlet.ShouldProcess($destination, 'Install AZ Touch skin and save rollback receipt')) { return }
$backup = New-BackupDirectory $vdjPath
$previous = $null
$previousHash = $null
if (Test-Path -LiteralPath $destination) {
    $previous = Join-Path $backup (Split-Path -Leaf $packagePath)
    Copy-Item -LiteralPath $destination -Destination $previous
    $previousHash = (Get-FileHash -LiteralPath $previous -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt = [ordered]@{
    Schema = 1; InstalledUtc = [DateTime]::UtcNow.ToString('o'); VirtualDJHome = $vdjPath;
    Destination = $destination; InstalledHash = $hash; PreviousPackage = $previous; PreviousHash = $previousHash
}
$receiptPath = Join-Path $backup 'install-receipt.json'
$receipt | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8
New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
$staged = Join-Path (Split-Path -Parent $destination) ([guid]::NewGuid().ToString('N') + '.tmp')
try {
    Copy-Item -LiteralPath $packagePath -Destination $staged
    if ((Get-FileHash -LiteralPath $staged -Algorithm SHA256).Hash.ToLowerInvariant() -ne $hash) { throw 'Staged package failed verification.' }
    Move-Item -LiteralPath $staged -Destination $destination -Force
} finally {
    if (Test-Path -LiteralPath $staged) { Remove-Item -LiteralPath $staged }
}
Write-Output "Installed: $destination"
Write-Output "Rollback receipt: $receiptPath"
Write-Output 'Open VirtualDJ -> Settings -> Interface -> select AZ Touch. Validate with cloned media before performing.'
