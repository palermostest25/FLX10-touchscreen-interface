[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$DriveRoot)
$ErrorActionPreference = 'Stop'
$legacy = Test-Path (Join-Path $DriveRoot 'PIONEER/rekordbox/export.pdb')
$oneLibrary = Test-Path (Join-Path $DriveRoot 'PIONEER/rekordbox/exportLibrary.db')
[pscustomobject]@{
    LegacyDeviceLibrary = $legacy
    OneLibrary = $oneLibrary
    MixxxLibraryRoute = $(if ($legacy) { 'Legacy library found; test playlists, cues and grids on a clone.' } elseif ($oneLibrary) { 'OneLibrary only: Mixxx cannot import this database. Keep your original USB unchanged.' } else { 'No standard rekordbox export database found at this root.' })
}
