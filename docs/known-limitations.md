# Known limitations / release blockers

This build is a hardware validation candidate, not a tested VirtualDJ release.

| Area | Implementation / actual limit |
|---|---|
| VirtualDJ runtime | No Windows VirtualDJ installation is available here. XML follows published SDK 8 examples; parsing/rendering in the user's exact build is NOT RUN. The shipped default skin could not be extracted here; the official SDK custom-browser example was inspected instead. |
| Surface and FLX10 | No physical access. Audio/PFL, driver/firmware, licensing, deck-layer mapping, touch scrolling/coordinates and 60-minute endurance remain NOT RUN. |
| OneLibrary | Uses the native VirtualDJ browser only. No USB/import parser is added. Exact rekordbox OneLibrary-only and dual-library import, cue/grid fidelity, artwork and unplug recovery remain NOT RUN and release-blocking. |
| Playing-deck loads | Explicit skin buttons test that target deck's `play` state. No touch live-load override. Native browser load gestures and factory hardware LOAD require the separate host `loadSecurity` option and a physical test. |
| Waveform lock | Native scratchwave/songpos are followed by no-op transparent buttons with explicit hit rectangles. This is an input-shield implementation, not a runtime-proven guarantee. T07 must pass for tapping/dragging/multitouch/right-click; otherwise revert to stock UI. Seeking is disabled at all times by design. |
| Deck state | Values come from host getters. Empty titles, unavailable BPM/key or cues remain host-defined. EMPTY/NO TRACK LOADED indicates `not loaded`. An offline/disconnected file can remain logically loaded, so EMPTY is not a media-health test. |
| Source health | The native folder path/tree is real. No reliable documented drive-presence subscription was implemented. There is no custom USB-connected/error banner, detection watcher or rescan. Native host errors are the only media-error feedback. Source label does not certify media readability. |
| Browse columns | Native browser uses requested larger font/line spacing. User configures columns. No bespoke per-row artwork/waveform or guaranteed absolute 9 mm touch size. Actual physical size depends on host scaling/DPI. |
| Search keyboard | Uses documented `search & show_keyboard` and native search field. Windows automatic touch keyboard invocation is not proven. Taskbar Touch keyboard remains a manual alternative. |
| Cue metadata | Native %namecueN and markers show host cue names/positions. Fixed slot colors follow the AZ convention; they do not certify imported rekordbox color/A–H/memory-cue fidelity. Empty fallback letters are display labels only. Cues are passive; fidelity needs G3. |
| Quantize / sync | Q reflects native quantize queries. SYNC uses is_sync; MASTER uses masterdeck. Passive feedback, not new sync/beatlock commands. User has not tried sync; no failure is observed. No on-air or Slip claim. |
| Time and views | Time-format toggle is documented VDJScript but not executed here. Display_time may be shared by decks in some host configurations. Two-deck views are fixed pairs 1+2 or 3+4, not a dynamically detected hardware layer. |
| FX / preview | Optional screen FX and prelisten omitted until trustworthy feedback/headphone routing can be tested. FLX10 FX and pads remain controlled by the native mapper. No helper, plugin, background service or cloud runtime is needed. |
| Tag List / Playlist | Tag List is VirtualDJ's local sidelist, not a Pioneer USB tag list. ADD TO TAG and target load focus must be tested. Playlist is native folder navigation, not a direct pinned-playlist shortcut. |
| Persistence | Startup selects two waves (1+2), four strips. No sound/settings forced by oninit. Explicit color/zoom taps change host display preferences; package rollback does not restore them. |
| Preview / screenshots | No VirtualDJ screenshots exist yet. Empty-state diagrams and populated design studies are labeled; illustrative data/wave shapes never ship in skin assets and are not G4/G5 evidence. Package preview remains omitted. |
| AZ palette / frequency bands | AZ COLORS uses documented blue/orange/ivory stem shapes. FREQUENCY COLORS uses host frequency coloring and host palette. Exact AlphaTheta three-band rendering is not proven. See [waveform-modes.md](waveform-modes.md). |
| Installer | File operations tested in PowerShell on a Linux temporary fixture where available; real Windows home discovery, OneDrive paths and process detection need Windows testing. Normal installation copies a ZIP only. Rollback restores/removes that ZIP, not settings selection. |

No library format conversion, vendor firmware, proprietary assets, custom audio
engine, custom mapper, native plugin, process hook, purchase or paid licence
activation is part of this build. A plugin would not establish the missing
physical evidence; no plugin is needed to attempt the next validation gates.

To progress: install the spike on the Surface, record the exact VirtualDJ build,
capture its four SDK proofs, then validate stock FLX10/USB and the main skin using
[the checklist](hardware-validation.md). Share failures with the command/action,
versions and screenshots. Keep the original USB detached while testing.
