# Hardware acceptance checklist

Execute on the Surface using a cloned test USB. All target procedures are currently NOT RUN.

| ID | Procedure | Pass condition |
|---|---|---|
| T01 | Start VDJ with skin installed; disconnect FLX10 then reconnect. | Correct skin loads, sensible hardware status, no crash. |
| T02 | Run with FLX10 powered on; check master and PFL outputs. | Four audio channels route correctly. |
| T03 | Insert cloned rekordbox USB with OneLibrary playlists. | Playlists and audio files can be browsed in app, no import wizard required unless VDJ itself requires one. |
| T04 | Compare 10 tracks with rekordbox export metadata. | Cues, grids, BPM/key and titles agree or documented source-specific deviations are flagged. |
| T05 | Load four tracks; start/play/pause all decks independently. | All display states and waveform positions sync correctly. |
| T06 | Use left deck select 1↔3, right 2↔4 and jog wheels. | Correct decks move, no cross-assignment. |
| T07 | Play deck 1 then touch waveform repeatedly. | No unintended seek/scratch during playback. |
| T08 | Tap SOURCE, BROWSE, PLAYLIST, SEARCH, WAVEFORM. | Tabs open working features; no dead controls. |
| T09 | Scroll 200+ track browser by finger and browse encoder. | Selectable rows and scroll respond smoothly. |
| T10 | Search from on-screen Windows touch keyboard. | Results filter properly; selected item can load to an intended deck. |
| T11 | Attempt to load another song into a playing deck. | Safety guard prevents unexpected audio interruption. |
| T12 | Switch 2-deck / 4-deck while tracks play. | Screen transitions without audio hiccup or deck reset. |
| T13 | Use hot cues and loops from FLX10. | Screen markers and state reflect actual deck. |
| T14 | Change FLX10 Beat FX and open FX overlay. | State accurate, or unsupported panel honestly hidden. |
| T15 | Test Windows scaling 150%, 175%, 200%, fullscreen. | Correct touch hitboxes, readability and no cropping in supported modes. |
| T16 | Exit/reopen app and disconnect USB safely. | Skin remembered where appropriate; preserved user data; no corrupt playlists. |
| T17 | Play for 60 minutes, four-deck realistic load. | No UI hangs, audio dropouts caused by skin, or runaway CPU. |
| T18 | Use app with Wi-Fi off. | Offline local/USB core workflow still works as supported by VDJ and licensing state. |
| T19 | Restore original skin and mapper. | Rollback succeeds in under a few steps; no database loss. |
| T20 | Check file safety before/after via hashes/snapshots of test drive. | No silent writes to user's original USB; any changes to cloned test drive explained. |

For each result record PASS / FAIL / BLOCKED / NOT RUN, UTC timestamp, host/build,
evidence path and exact reproduction steps. NOT RUN is not a pass.

Add these route-specific checks to T07/T11:

- T07: playing and paused, tap/drag/double-tap/right-click/long-press/two-finger
  gesture on scratchwave, songpos and cue markers. No movement should occur.
- T11: explicit skin LOAD on each deck, native browser double-click and drag/drop,
  each physical hardware LOAD button on both layers. Test host loadSecurity.
- T12: switch every page and deck-pair view during playback. Check all deck
  positions, effects, faders and audio routing remain unchanged.
- T19: first-install removal and replacement rollback; compare settings, mapper
  and database hashes to confirm they were not changed by the scripts.

T14 has no AZ Touch FX panel in this candidate. Record the panel as not
implemented; independently verify native FLX10 FX behavior.
