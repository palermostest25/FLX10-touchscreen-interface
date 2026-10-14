# Cross-platform file-operation regression fixture; Windows host tests remain separate.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$tools = Join-Path $repo 'tools'
$temp = Join-Path ([IO.Path]::GetTempPath()) ('az-touch-fixture-' + [guid]::NewGuid().ToString('N'))
$homePath = Join-Path $temp 'VirtualDJ space'
New-Item -ItemType Directory -Path $homePath -Force | Out-Null
Set-Content -LiteralPath (Join-Path $homePath 'settings.xml') -Value '<settings>sentinel</settings>'
New-Item -ItemType Directory -Path (Join-Path $homePath 'Mappers') | Out-Null
Set-Content -LiteralPath (Join-Path $homePath 'Mappers/original.xml') -Value 'do not change'
$settingsHash = (Get-FileHash -LiteralPath (Join-Path $homePath 'settings.xml')).Hash
$mapperHash = (Get-FileHash -LiteralPath (Join-Path $homePath 'Mappers/original.xml')).Hash
$skinPath = Join-Path $homePath 'Skins/AZ-Touch-3x2.zip'
$package = Join-Path $repo 'dist/AZ-Touch-3x2.zip'
$checks = 0

function Assert-True([bool] $Condition, [string] $Message) {
    if (-not $Condition) { throw "FAIL: $Message" }
    $script:checks++
}
function Assert-Throws([scriptblock] $Action, [string] $Pattern) {
    $threw = $false
    try { & $Action | Out-Null } catch {
        if ($_.Exception.Message -notmatch $Pattern) { throw }
        $threw = $true
    }
    Assert-True $threw "Expected rejection: $Pattern"
}
function Latest-Receipt {
    return (Get-ChildItem -LiteralPath (Join-Path $homePath 'AZTouch-backups') -Recurse -Filter 'install-receipt.json' |
        Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1).FullName
}
try {
    # Parse each script before running it.
    foreach ($f in @(Get-ChildItem -LiteralPath $tools -Filter '*.ps1')) {
        $tokens = $null; $parseErrors = $null
        [void][Management.Automation.Language.Parser]::ParseFile($f.FullName,[ref]$tokens,[ref]$parseErrors)
        Assert-True ($parseErrors.Count -eq 0) "Parse $($f.Name)"
    }
    & (Join-Path $tools 'install_windows.ps1') -VirtualDJHome $homePath -WhatIf | Out-Null
    Assert-True (-not (Test-Path -LiteralPath $skinPath)) 'WhatIf created no skin'
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $homePath 'AZTouch-backups'))) 'WhatIf created no backup'
    & (Join-Path $tools 'install_windows.ps1') -VirtualDJHome $homePath | Out-Null
    Assert-True ((Get-FileHash -LiteralPath $skinPath).Hash -eq (Get-FileHash -LiteralPath $package).Hash) 'First install copied exact package'
    $firstReceipt = Latest-Receipt
    Assert-Throws { & (Join-Path $tools 'install_windows.ps1') -VirtualDJHome $homePath } 'already present'
    & (Join-Path $tools 'restore_default.ps1') -ReceiptPath $firstReceipt -WhatIf | Out-Null
    Assert-True (Test-Path -LiteralPath $skinPath) 'Rollback WhatIf leaves skin'
    & (Join-Path $tools 'restore_default.ps1') -ReceiptPath $firstReceipt | Out-Null
    Assert-True (-not (Test-Path -LiteralPath $skinPath)) 'First install rollback removes only skin'
    Assert-Throws { & (Join-Path $tools 'restore_default.ps1') -ReceiptPath $firstReceipt } 'already absent'
    # An existing skin must be backed up and recover byte-for-byte.
    Set-Content -LiteralPath $skinPath -Value 'previous skin bytes'
    $oldHash = (Get-FileHash -LiteralPath $skinPath).Hash
    & (Join-Path $tools 'install_windows.ps1') -VirtualDJHome $homePath -Replace | Out-Null
    $replaceReceipt = Latest-Receipt
    Add-Content -LiteralPath $skinPath -Value 'tampered'
    Assert-Throws { & (Join-Path $tools 'restore_default.ps1') -ReceiptPath $replaceReceipt } 'changed since'
    Copy-Item -LiteralPath $package -Destination $skinPath -Force
    & (Join-Path $tools 'restore_default.ps1') -ReceiptPath $replaceReceipt | Out-Null
    Assert-True ((Get-FileHash -LiteralPath $skinPath).Hash -eq $oldHash) 'Replacement rollback restores old bytes'
    # Corrupt download must be rejected before writing a skin/receipt.
    $badDist = Join-Path $temp 'corrupt-download'
    New-Item -ItemType Directory -Path $badDist | Out-Null
    Copy-Item -LiteralPath $package -Destination (Join-Path $badDist 'AZ-Touch-3x2.zip')
    Copy-Item -LiteralPath (Join-Path $repo 'dist/SHA256SUMS.txt') -Destination $badDist
    Add-Content -LiteralPath (Join-Path $badDist 'AZ-Touch-3x2.zip') -Value 'corrupt'
    Assert-Throws { & (Join-Path $tools 'install_windows.ps1') -VirtualDJHome $homePath -SkinZip (Join-Path $badDist 'AZ-Touch-3x2.zip') -Replace } 'checksum mismatch'
    Assert-True ((Get-FileHash -LiteralPath $skinPath).Hash -eq $oldHash) 'Corrupt install leaves old skin'
    & (Join-Path $tools 'backup_windows.ps1') -VirtualDJHome $homePath | Out-Null
    $snapshots = @(Get-ChildItem -LiteralPath (Join-Path $homePath 'AZTouch-backups') -Recurse -Filter 'settings.xml')
    Assert-True ($snapshots.Count -eq 1) 'Backup contains local settings'
    Assert-True ((Get-FileHash -LiteralPath $snapshots[0].FullName).Hash -eq $settingsHash) 'Backup is byte-exact'
    Assert-True ((Get-FileHash -LiteralPath (Join-Path $homePath 'settings.xml')).Hash -eq $settingsHash) 'Settings unchanged'
    Assert-True ((Get-FileHash -LiteralPath (Join-Path $homePath 'Mappers/original.xml')).Hash -eq $mapperHash) 'Mapper unchanged'
    Write-Output "PASS: $checks script assertions (temporary fixture only; Windows/VirtualDJ NOT RUN)."
} finally {
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
}
