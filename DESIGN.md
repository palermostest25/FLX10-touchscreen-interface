# AZ Touch visual authority

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
