# Mixxx companion screen

Mode: Operate. Extend the existing GPL XDJ OPEN SOURCE skin, preserving its AZ/RX3
composition and native host behaviour. Source: `mixxx/AZ Touch`.

The user wants an actual XDJ-AZ-like display on a Surface Pro 7, with the FLX10
doing mixing and transport. Three frequency bands, grids crossing the rolling
waves, credible native state and a complete free setup matter more than new
decorative UI. Do not present generated screenshots as host output.

Target: Windows, 2736 × 1824 landscape at 200% scaling, effective 1368 × 912;
minimum logical area 1100 × 700. No mobile-web surface is shipped. Current runtime
evidence is Linux Mixxx 2.5.0 at 1368 × 912, generated calibration audio, virtual
PulseAudio sink with timestamp/underflow warnings. Target Windows stable is 2.5.6.
Clean audio, audible sync, latency and CPU headroom are unverified. Physical
Surface touch, FLX10 MIDI/audio and rekordbox USB tests are not run; see
[validation scope](mixxx-validation.md).

Invariants: native Mixxx rolling/overview renderers; blue lows #1678ff, orange
mids #f6a21a, ivory highs #f7f1dd; black ground, charcoal cells, white type,
Segoe UI with DejaVu Sans fallback. Fixed playheads and visible native beat grids.
Three views: 1+2, 3+4, and four waves in 3/1/2/4 order. Four summaries always remain.
The three 110 × 48 logical-pixel view buttons disable the active choice, keeping
repeated taps from toggling it off and cycling the native stack.

Library/setup summaries retain explicit DECK 1–4 labels and native, right-elided
track titles in 24px headers with 13px text. Time, overview and BPM sit below.
Browse/Back use 14px labels on 100 × 48 targets. These final review corrections
preserve the existing flat composition and make deck identity visible in Browse.

Touch/mouse/drop are disabled on waves and overviews. This is statically checked
in Qt properties, with paused mouse-drag protection observed in the native host;
finger gestures still need the Surface check. Explicit load buttons disable for
playing decks; the installer also enables Mixxx's native playing-track load lock.
The Linux host refused both a disabled load button and the native keyboard load
while playing. Physical hardware LOAD is untested. FLX10 transport, pitch, EQ and
cues belong to the separately downloaded MIDI mapping.

Native FX are a secondary compact panel; hardware labels do not recreate Pioneer
algorithms. Original skin work remains credited under GPL v3. No new audio engine,
no fake controller-presence banner, no claim of OneLibrary support, no promises of
jog-screen waveforms, stems, DMX or Mix Point Link. Detailed preferences remain
native Mixxx dialogs. No HTML/CSS detector applies to this Qt XML/QSS surface.

Source/licensing: [upstream and dated modifications](../mixxx/UPSTREAM.md) and
[component notices](../THIRD_PARTY_NOTICES.md). Original MIT utilities, the GPL
skin and the separately downloaded mapping keep their respective terms.
