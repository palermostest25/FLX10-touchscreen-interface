# AZ Touch

Current primary development route (2026-10-15): free Mixxx stable with a GPL
adaptation of Marc Monka's XDJ OPEN SOURCE skin in `mixxx/AZ Touch`. The original
VirtualDJ candidate below is retained as an alternative. `README.md` covers Mixxx;
`README-VirtualDJ.md` retains the previous complete instructions. See
`docs/best-route.md` for evidence and `docs/mixxx-surface.md` for the native surface.
Mixxx does not meet the original OneLibrary-only USB requirement. Never conceal
that gap or change the user's original USB. Windows/FLX10 tests remain outstanding.

For Mixxx, target Windows stable 2.5.6 at the Surface's effective 1368×912 area.
Native Qt XML/QSS owns the display: 1+2, 3+4 and four-wave views, four labelled
deck summaries on every page, protected waveforms and explicit guarded loads.
The FLX10's separately downloaded MIDI mapping owns transport and mixing.
Linux Mixxx 2.5.0 runtime captures use synthetic calibration audio and a virtual
PulseAudio sink with underflow warnings; they establish native UI operation,
not clean audio, audible sync or physical Surface/FLX10/USB compatibility.

Native VirtualDJ skin for a Surface Pro 7 and DDJ-FLX10. Target resolution
2736×1824, landscape 3:2; source canvas 1368×912. Hardware handles audio,
transport, EQ, cues and sync through the factory mapper. Native engine owns
waveforms, track state and USB/database browsing.

User's current priority: make the screen resemble the real XDJ-AZ layout and
blue/orange/ivory waveform treatment. No actual sync failure was reported; the
user has not tried the skin yet. Preserve native behavior and report hardware
testing as NOT RUN. Do not build a new audio engine or present a diagram as
proof that VirtualDJ ran.

Required workflows: native USB browsing, explicit safe loads to four decks,
two/four scrolling-wave views, four deck strips at all times, clear Settings
and offline playback delegated to the host. Original USBs stay unchanged;
target validation uses clones. Paid host licensing is a separate known dependency.
