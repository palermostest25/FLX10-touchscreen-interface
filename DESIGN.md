# AZ Touch visual authority

The current Mixxx adaptation inherits the same pinned AZ composition. Its native
surface contract and concrete colour tokens are in `docs/mixxx-surface.md`.
Native XML/QSS uses black/charcoal, Segoe UI with DejaVu Sans fallback, and real
3-Band waves: blue lows `#1678ff`, orange mids `#f6a21a`, ivory highs `#f7f1dd`.
Keep the 1+2, 3+4 and four-wave modes, four labelled summaries, fixed playheads
and native beat grids. Library/setup summaries retain a 24px header with 13px
DECK/title text; Browse/Back labels are 14px. The selected wave-view button stays
disabled so a repeated tap retains the current view. Waveforms and overviews
remain protected from input/drops; load buttons disable while their deck plays.

The sections below continue to document the retained VirtualDJ implementation;
its stem-colour limitation must not be confused with Mixxx's real 3-Band renderer.

Mode: Operate. Refinement follows the actual XDJ-AZ screen, rather than generic
UI cards or the Touchy developer's interpretation. Product truth is in PRODUCT.md.

Reference inspected: the real AZ waveform screenshot linked in the user's HTML
handoff, showing per-waveform metadata at left, long blue/orange/ivory waves,
hot-cue labels across the middle and compact lower strips with title, time,
overview and a right-aligned BPM column. The Surface's taller 3:2 display and
native host navigation require adaptation rather than distorted scaling.

Keep: near-black background, flat charcoal cells, square boundaries, white
technical text, blue focus, orange master BPM, slot-colored cue letters, large
time numerals. Fonts use the Windows/VirtualDJ-supported Segoe UI family.
Avoid large branded card tiles, decorative gradients, rainbow colors forced
by XML, fake FX panels or hardware-presence labels.

Native AZ COLORS chooses documented Shapes with blue/orange/ivory component
colors. Those are stem components, not proven frequency-separated bands.
FREQUENCY COLORS explicitly chooses native Colors and waveUseFrequency; its
palette is host-controlled. Do not conceal that technical distinction.

Source of truth is tools/build_skin.py. Offline preview images are labeled
design studies; their sample track data and wave shapes never ship in the skin.
Actual host render screenshots are still unavailable. Inspect two/four views
together, fix visible issues in one batch and confirm once.
