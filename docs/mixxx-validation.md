# Mixxx candidate validation — 2026-10-15 UTC

Candidate: Mixxx skin 0.1.0. This report separates native-host observations,
file-operation/script checks and physical hardware checks. No FLX10, Surface,
Windows installation or rekordbox USB was attached to this environment.

## Native host actually run

- Debian 13, native Debian Mixxx **2.5.0+dfsg-3+b1**, Qt 6.8.2.
  Windows target is stable **2.5.6**; it was source-inspected, not executed.
- Isolated settings directory and Xvfb screen **1368 × 912**, representing the
  Surface’s logical area at 200% scaling. No tablet or touch events were emulated.
- Actual native OpenGL **3-Band (all-shaders)** renderer, type 19, and 3-Band
  overview. Palette is blue low frequencies, orange mids, ivory highs.
- Four generated 32-second WAVs, labelled SYNTHETIC, nominal BPMs 120/124/128/132.
  Reproduce them with `python tools/generate_mixxx_test_audio.py OUTPUT_DIRECTORY`.
  Their repeated pulse shapes are properties of the calibration audio; no waveform
  pixels or fake song metadata are drawn by this skin.
- Audio used a **virtual PulseAudio null sink** through ALSA. Logs contain
  virtual-device timestamp and underflow warnings. This establishes engine/UI
  operation only; **clean audio playback, audible sync, CPU headroom and latency
  are NOT VERIFIED**.

## Observations and checked behaviour

| Check | Result and scope |
|---|---|
| Native skin loads | PASS on Linux 2.5.0; screenshots captured from the process |
| Three native frequency bands | PASS, blue/orange/ivory visible with native analysis |
| Vertical beat grid and fixed playheads | PASS, visible on rolling waves |
| 1+2 / 3+4 / four-wave navigation | PASS using real UI clicks; four-wave order 3/1/2/4 |
| Repeated view taps and return navigation | PASS for all three choices: repeated tap and switch away/back keep the correct view; [record](research/mixxx-view-repeat-check.json) |
| Native time, BPM, key and overview | PASS on calibration tracks; time advanced during engine playback |
| BPM sync action | Native keyboard action matched deck 1’s 120 to deck 2’s 124 and showed changed pitch; this is NOT physical SYNC or audible beat-lock proof |
| Waveform mouse-drag protection | PASS paused: rolling and overview crops remained pixel-identical after drags; [record](research/mixxx-mouse-lock-check.json) |
| Playing-deck load protection | PASS on Linux: with 132 selected and deck 1 playing 120, LOAD 1 was disabled and Shift+Left did not replace it; after pause, LOAD 1 loaded 132 |
| Four summaries in library/setup | Native strips present; independent review requested persistent deck IDs/titles and larger Browse/Back labels; corrected and recaptured |
| Surface touch/drop behaviour | NOT RUN; disabled Qt input/drop properties checked statically, mouse protection checked at runtime |

The [load-guard capture](screenshots/mixxx-load-guard-runtime.png) shows the
disabled LOAD 1 and unchanged 120 BPM while a 132 BPM track is selected. The later
paused click changed deck 1 to 132. Its layout predates the review’s added mini
strip headers; it is behaviour evidence, not the latest visual reference.

Latest visual references, all native 1368 × 912 captures:

- [1+2](screenshots/mixxx-two-runtime.png)
- [3+4](screenshots/mixxx-pair34-runtime.png)
- [Four waves](screenshots/mixxx-four-runtime.png)
- [Library](screenshots/mixxx-library-runtime.png)

The four calibration tracks have no prepared hotcues. These captures therefore
do not validate imported cue positions, colours or labels. The waveforms and
times are real Mixxx state; visual appearance with actual music will vary.

Independent review scored all three concrete findings resolved: library deck
IDs/titles, readable Browse/Back labels, and stable active-view selection. Its
final disposition was **ship, scoped to those fixes**, as a hardware-validation
candidate. This is not a hardware qualification or a claim that no other issues exist.

## Automated checks actually executed

Executed in Linux, not Windows:

- **18 Python tests**, including retained VirtualDJ artifact checks and five
  new Mixxx structural/safety checks: PASS.
- **16 Mixxx PowerShell fixture assertions**, PowerShell 7.6.7: PASS, including
  the live pinned-file downloads, SHA-256 checks, preset/script-reference update,
  preservation of unrelated config/mappings, exact rollback and USB-format cases.
- **22 retained VirtualDJ PowerShell fixture assertions**: PASS.
- Selected MIDI-only mapping XML: **439 inputs, zero duplicate addresses,
  no missing functions among 25 distinct script bindings**. [Audit](research/veezuhz-midi-only-audit.json).
- JavaScript parses with Node; a VM stub exercised init and eight endpoints
  across four 14-bit tempo faders: PASS. Stub APIs cannot establish physical MIDI,
  Qt script instantiation, scratch timing or controller feedback.
- Loui’s separate mapping: 13 colliding input addresses detected. This is a
  source-audit finding, not a physical failure report. [Audit](research/loui-midi-audit.json).

Commands:

```sh
python tools/build_mixxx_skin.py
python tools/build_skin.py
python -m unittest discover -s tests -p 'test_*.py'
pwsh -NoProfile -File tests/test_mixxx_windows.ps1 -Network
pwsh -NoProfile -File tests/test_windows_scripts.ps1
python tools/audit_mixxx_mapping.py PATH/TO/Pioneer-DDJ-FLX10.midi.xml
node tests/test_mixxx_mapping.js PATH/TO/Pioneer-DDJ-FLX10-scripts.js
```

The mapping commands require the selected MIDI-only files downloaded separately;
they are not distributed here. The skin archive is deterministic and includes its
editable source, modification notice and GPL licence. Package checksum is in
`dist/mixxx/SHA256SUMS.txt`.

## Physical acceptance checklist — all still NOT RUN

- [ ] Install stable Windows 2.5.6, select AZ Touch, verify scaling/fullscreen at 200%.
- [ ] Enable only the selected FLX10 MIDI mapping; inspect Mixxx logs for exceptions.
- [ ] Verify all four decks’ play/cue, deck select, tempo direction/range and keylock.
- [ ] Verify jog touch/scratch, release, nudge and vinyl mode without jumps.
- [ ] Verify faders, gain/EQ, crossfader assignment, CUE LEDs and meters.
- [ ] Confirm ASIO main 1–2/headphones 3–4 with the physical headphone mix and speakers.
- [ ] Test a sustained local four-deck mix; record buffer, CPU and audio dropouts.
- [ ] Test real SYNC short/long presses and audible alignment over time; check leader feedback.
- [ ] Verify loops, pad modes, hotcue colours and feedback on every deck.
- [ ] Test all finger taps/drags across waves and overview while paused and playing.
- [ ] Confirm touchscreen loads and hardware LOAD cannot replace a playing track.
- [ ] Verify Browse/Back/Setup and track selection on the Surface without a keyboard.
- [ ] On a clone: detect legacy export, inspect playlists/cues/grids and compare tracks to rekordbox.
- [ ] Test clone removal/reinsertion and missing-media behaviour without the original drive attached.
- [ ] Restore the saved Windows backup and confirm previous skin/mapping/config return.

OneLibrary-only import is unsupported, not a pending test expected to pass.
Changing/exporting a drive requires a separate user decision; the installer and
format checker do not do it. Jog-screen waveforms, stems, DMX and Mix Point Link
are outside this candidate’s promises.
