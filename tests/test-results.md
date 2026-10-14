# Test results — 0.1.0 hardware candidate

Report UTC: 2026-10-14T09:59:56+00:00

## Executed engineering checks

Host: `Linux-6.18.44-x86_64-with-glibc2.41`; Python 3.12.14, Pillow 11.3.0, PowerShell 7.6.7.

| Check | Result | Evidence / scope |
|---|---|---|
| XML/PNG packaging and geometry | PASS | tools/build_skin.py and tools/validate_skin.py: both flat SDK 8 archives, four declared decks, canvas/assets/panel references/guard coverage |
| Regression suite | PASS | python -m unittest discover -s tests -v: 11 tests, including reject-on-mutation safety cases and reproducible rebuild |
| PowerShell syntax/file operations | PASS | pwsh -NoProfile -File tests/test_windows_scripts.ps1: 19 assertions, temporary fixture only; no real Windows or VirtualDJ |
| Actual VirtualDJ parser/rendering | NOT RUN | No Windows host installed |
| Installed default skin extraction | NOT RUN | Official SDK example inspected instead |

The script fixture proves exact install/copy, WhatIf behavior, replace refusal,
backup restoration, changed-skin refusal, checksum rejection, local snapshot and
unchanged settings/mapper sentinel files. It does not test Windows auto-discovery,
OneDrive, OS process detection, live controller safety or the audio engine.

## Artifact checksums

```text
a3371fc971b777ff642e71d19b6c295350baaf06c3d4eb9335a45b60628a50ce  AZ-Touch-3x2.zip
19c9f15bbfb77958ef41956347d411c0fcff2ee0ffe19fb02fdb930adda81a06  AZ-Touch-SDK-Spike.zip
```

## Target acceptance results

Target Windows/VirtualDJ build, audio driver, firmware, licence and USB versions:
**UNKNOWN**. Target timestamps/evidence: **none**. G0–G5 are BLOCKED by absent
physical access. T01–T20 are NOT RUN; unsupported features are noted separately.

| ID | Procedure | Status | Target time / evidence / notes |
|---|---|---|---|
| T01 | Start VDJ with skin installed; disconnect FLX10 then reconnect. | NOT RUN | No target access; no screenshot/log. |
| T02 | Run with FLX10 powered on; check master and PFL outputs. | NOT RUN | No target access; no screenshot/log. |
| T03 | Insert cloned rekordbox USB with OneLibrary playlists. | NOT RUN | No target access; no screenshot/log. |
| T04 | Compare 10 tracks with rekordbox export metadata. | NOT RUN | No target access; no screenshot/log. |
| T05 | Load four tracks; start/play/pause all decks independently. | NOT RUN | No target access; no screenshot/log. |
| T06 | Use left deck select 1↔3, right 2↔4 and jog wheels. | NOT RUN | No target access; no screenshot/log. |
| T07 | Play deck 1 then touch waveform repeatedly. | NOT RUN | No target access; no screenshot/log. |
| T08 | Tap SOURCE, BROWSE, PLAYLIST, SEARCH, WAVEFORM. | NOT RUN | No target access; no screenshot/log. |
| T09 | Scroll 200+ track browser by finger and browse encoder. | NOT RUN | No target access; no screenshot/log. |
| T10 | Search from on-screen Windows touch keyboard. | NOT RUN | No target access; no screenshot/log. |
| T11 | Attempt to load another song into a playing deck. | NOT RUN | No target access; no screenshot/log. |
| T12 | Switch 2-deck / 4-deck while tracks play. | NOT RUN | No target access; no screenshot/log. |
| T13 | Use hot cues and loops from FLX10. | NOT RUN | No target access; no screenshot/log. |
| T14 | Change FLX10 Beat FX and open FX overlay. | NOT RUN | FX overlay not implemented; native FLX10 FX still needs testing. |
| T15 | Test Windows scaling 150%, 175%, 200%, fullscreen. | NOT RUN | No target access; no screenshot/log. |
| T16 | Exit/reopen app and disconnect USB safely. | NOT RUN | No target access; no screenshot/log. |
| T17 | Play for 60 minutes, four-deck realistic load. | NOT RUN | No target access; no screenshot/log. |
| T18 | Use app with Wi-Fi off. | NOT RUN | No target access; no screenshot/log. |
| T19 | Restore original skin and mapper. | NOT RUN | File operations passed Linux fixture; real Windows/manual skin selection NOT RUN. |
| T20 | Check file safety before/after via hashes/snapshots of test drive. | NOT RUN | No target access; no screenshot/log. |

Failures on target must include exact reproduction steps and stock-skin comparison.
Hardware PASS requires actual evidence; do not substitute these engineering checks.

## Reproduce engineering checks

```text
python tools/build_skin.py
python tools/validate_skin.py
python -m unittest discover -s tests -v
pwsh -NoProfile -File tests/test_windows_scripts.ps1
```

Use Windows PowerShell 5.1 or PowerShell 7 for the script fixture on Windows.
After any generator change, regenerate archives/checksums/ledger and update this report.
