# USB source compatibility report

**Observed compatibility: NOT RUN for every source below.** No rekordbox USB,
Surface or VirtualDJ host is attached to the build environment. The skin delegates
all discovery, database parsing and errors to the native browser/engine.

| Source/export | Playlists | File playback | Cues | Beatgrid/BPM/key | Evidence |
|---|---|---|---|---|---|
| rekordbox OneLibrary only | NOT RUN | NOT RUN | NOT RUN | NOT RUN | None |
| rekordbox OneLibrary + legacy Device Library | NOT RUN | NOT RUN | NOT RUN | NOT RUN | None |
| Legacy Device Library only | NOT RUN | NOT RUN | NOT RUN | NOT RUN | None |
| Local rekordbox collection | NOT RUN | NOT RUN | NOT RUN | NOT RUN | None |
| Local filesystem music | NOT RUN | NOT RUN | NOT RUN | NOT RUN | None |

Record per test: UTC timestamp, Windows/VirtualDJ/rekordbox versions, USB model,
filesystem, drive letter, export type, hardware write-blocking status, initial
file/hash snapshot and write-protection settings. Include a screenshot showing
native OneLibrary → actual drive → actual playlist and a selected file path.

## Read protection

VirtualDJ's official `readOnly` option states that databases on drives will not
be modified. It is narrower than operating-system write protection. Disable
OneLibrary Auto sync cue points and Auto generate stems for both the folder and
drive. Avoid all export/copy/convert/database-create/edit actions. Local settings,
history and other host files may still change. This skin does not issue USB write
commands, but it cannot certify that the application never writes to a drive.

Keep the original detached. Use a clone and compare all clone files/hashes before
and after the test. Record any created/modified/deleted file and its purpose.
Do not mark T20 PASS merely because the skin source lacks an export action.

## Ten-track fidelity record

Choose varied MP3/WAV/FLAC/AAC tracks as supported, short and long names,
different BPMs/keys and multiple cue types. Replace the blank rows with measured
results; compare the USB export against VirtualDJ, not the skin artwork.

| Track | Physical USB path | Title/artist/artwork | BPM/grid/key | Hot cue labels/positions/colors | Memory cues | Result/evidence |
|---|---|---|---|---|---|---|
| 01 | — | — | — | — | — | NOT RUN |
| 02 | — | — | — | — | — | NOT RUN |
| 03 | — | — | — | — | — | NOT RUN |
| 04 | — | — | — | — | — | NOT RUN |
| 05 | — | — | — | — | — | NOT RUN |
| 06 | — | — | — | — | — | NOT RUN |
| 07 | — | — | — | — | — | NOT RUN |
| 08 | — | — | — | — | — | NOT RUN |
| 09 | — | — | — | — | — | NOT RUN |
| 10 | — | — | — | — | — | NOT RUN |

## Failure triage

1. Record the exact native tree/playlist/error. Verify the USB has the intended
   export and files using the original exporting software on the clone.
2. Compare current stock VirtualDJ with AZ Touch. If both fail, it is a host/source
   problem; if only AZ Touch fails, record a skin/browser reproduction.
3. Separate OneLibrary-only from dual-library results. Plain filesystem playback,
   M3U imports and legacy-only reads do not pass G2's primary OneLibrary requirement.
4. If dual export is needed, request the user's decision before changing that
   requirement and use only a duplicate USB. Do not convert/format the original.
5. Safe unplug while stopped and failure during playback are separate tests.
   Use cloned media, preserve other working decks, and record native errors and
   reconnect behavior; this skin does not implement disconnect recovery.

References: [VirtualDJ OneLibrary](https://virtualdj.com/manuals/virtualdj/interface/database/cdjexport.html),
[rekordbox OneLibrary FAQ](https://rekordbox.com/en/support/faq/onelibrary-7/),
[VirtualDJ options](https://virtualdj.com/manuals/virtualdj/appendix/optionslist.html).
