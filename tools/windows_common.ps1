Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-VirtualDJClosed {
    if (Get-Process -Name 'virtualdj*' -ErrorAction SilentlyContinue) {
        throw 'Close VirtualDJ before installing, backing up, or rolling back.'
    }
}

function Resolve-VirtualDJHome([string] $ExplicitPath) {
    if ($ExplicitPath) {
        $resolved = (Resolve-Path -LiteralPath $ExplicitPath).Path
        if (-not (Test-Path -LiteralPath $resolved -PathType Container)) { throw 'VirtualDJHome must be a directory.' }
        if (-not (Test-Path -LiteralPath (Join-Path $resolved 'settings.xml') -PathType Leaf)) {
            throw 'No settings.xml here. Start VirtualDJ once, close it, then provide its actual home folder.'
        }
        return $resolved
    }
    $candidates = @()
    $documents = [Environment]::GetFolderPath('MyDocuments')
    if ($documents) { $candidates += Join-Path $documents 'VirtualDJ' }
    if ($env:LOCALAPPDATA) { $candidates += Join-Path $env:LOCALAPPDATA 'VirtualDJ' }
    if ($env:APPDATA) { $candidates += Join-Path $env:APPDATA 'VirtualDJ' }
    $found = @($candidates | Select-Object -Unique | Where-Object {
        Test-Path -LiteralPath (Join-Path $_ 'settings.xml') -PathType Leaf
    })
    if ($found.Count -ne 1) {
        throw 'Could not choose one VirtualDJ home. Find the folder containing settings.xml and pass -VirtualDJHome "that path".'
    }
    return (Resolve-Path -LiteralPath $found[0]).Path
}

function Assert-Package([string] $ZipPath, [string] $ChecksumPath) {
    $expected = @('AZ-Touch-3x2.zip', 'AZ-Touch-SDK-Spike.zip')
    $name = Split-Path -Leaf $ZipPath
    if ($name -notin $expected) { throw 'Use one of the two distributed AZ Touch archives.' }
    $lines = @(Get-Content -LiteralPath $ChecksumPath | Where-Object { $_ -match ('^[a-fA-F0-9]{64}\s+' + [regex]::Escape($name) + '$') })
    if ($lines.Count -ne 1) { throw 'Missing or ambiguous SHA256SUMS entry.' }
    $hash = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne ($lines[0] -split '\s+')[0].ToLowerInvariant()) { throw 'Skin checksum mismatch. Download a clean copy.' }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        $xmlName = if ($name -eq 'AZ-Touch-3x2.zip') { 'az-touch.xml' } else { 'az-touch-spike.xml' }
        $entries = @($archive.Entries | ForEach-Object { $_.FullName })
        if ($entries.Count -ne 2 -or @($entries | Select-Object -Unique).Count -ne 2 -or
            $xmlName -notin $entries -or 'az-touch.png' -notin $entries) { throw 'Unexpected archive contents.' }
    } finally { $archive.Dispose() }
    return $hash
}

function New-BackupDirectory([string] $VdjPath) {
    $id = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8)
    $path = Join-Path (Join-Path $VdjPath 'AZTouch-backups') $id
    New-Item -ItemType Directory -Path $path -Force | Out-Null
    return $path
}
