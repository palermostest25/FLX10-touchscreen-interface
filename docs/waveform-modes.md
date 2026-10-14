# AZ palette and real frequency analysis are different

The visual target is the real XDJ-AZ screen's blue/orange/ivory waves and compact
player information. Prior builds forced `scratchwave color="full"`, selecting
the full-color renderer without the requested palette. 0.3.0 removes that forced
renderer and exposes two explicit native options.

| Control | Host changes made on that tap | What the colors mean |
|---|---|---|
| AZ COLORS | skinWaveformType → shapes; skinOverviewType → shapes | Blue/orange/ivory native shape components. The SDK calls these vocal/instrumental/beat, not low/mid/high frequency bins. |
| FREQUENCY COLORS | skinWaveformType → colors; skinOverviewType → colors; waveUseFrequency → on | Frequency-based coloring in the native Colors renderer; palette remains the host's coloredWaveforms scheme. |
| ZOOM − / + | Native zoom action | Shared visual zoom, no pitch/seek/transport command. |

Shape parameters: [Scratchwave SDK](https://virtualdj.com/wiki/Skin%20Scratchwave.html).
The palette approach is also described in the
[September 2026 skin discussion](https://virtualdj.com/forums/270039/VirtualDJ_Skins/Rekordbox_3_Band_color_waveform_XLM_edit_help..html).
The frequency switch and host palette are documented in the
[options list](https://virtualdj.com/manuals/virtualdj/appendix/optionslist.html)
and [waveform manual](https://virtualdj.com/manuals/virtualdj/interface/topsection/appcontrols/layout/waveform.html).

**Not proven here:** exact AlphaTheta frequency crossovers, band geometry,
gain normalization, scrolling or cue/phrase graphics. XML can select documented
native renderers; it cannot replace their analysis algorithms. Do not claim
recolored stem shapes are true three-frequency bands.

Factory FLX10 mappings and sync remain unchanged. SYNC is `is_sync` feedback,
not an invented Boolean. User clarified no sync failure has been observed;
the skin has not been tried. MASTER is native `masterdeck` feedback. No new
audio/sync command runs when switching pages.

Target validation: compare the same track in stock and AZ Touch Shapes/Colors,
record host build/settings, change EQ versus stems and record renderer response.
Verify native overlay/grid/playhead alignment in two/four views at every zoom.
Check the same cue/beat positions while phase-synchronized. All runtime tests
remain NOT RUN.

Offline populated images are explicitly labeled visual studies. Their example
track values, wave shapes and sync/master state are not in the skin XML/PNG ZIP.
