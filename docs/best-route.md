# Route decision — 2026-10-15

For **free software + an AZ-style touchscreen layout**, develop the existing
Mixxx skin, using the separate MIDI-only FLX10 mapping. This is the strongest
free candidate found, with an actual native host render now available.
It still needs Windows/FLX10 testing. It does **not** satisfy OneLibrary-only
USB import; that requirement remains a decision gate rather than an invented feature.

If the original brief’s OneLibrary requirement is absolute, keep VirtualDJ with
its already-working factory mapping, or trial djay Pro’s stock Hardware Mode.
Those routes have paid software requirements. No investigated route establishes
free use, exact AZ skinning, complete FLX10 behaviour and OneLibrary import together.

| Route | AZ/touch layout | FLX10 | Library/cost consequence | Decision |
|---|---|---|---|---|
| Mixxx 2.5.6 + XDJ skin adaptation | Native custom XML skin, real frequency bands/grids | Community MIDI mapping; Windows hardware test outstanding | Free; legacy rekordbox USB, not OneLibrary | Best free development route |
| VirtualDJ + existing candidate | Native skin engine; needs actual host visual validation | Factory mapping; user reports it worked flawlessly | FLX10 requires Pro for sustained use; OneLibrary still needs clone test | Strongest continuity with known controller setup |
| djay Pro Windows | Stock four-deck/Hardware Mode; arbitrary skins unsupported | Official FLX10 support | PRO subscription; documented OneLibrary import | Best trial if native OneLibrary outranks exact AZ layout |
| rekordbox / Serato DJ Pro | Stock desktop interfaces | Official FLX10 integration/core hardware unlock | Core controller use available with FLX10; feature tiers vary | Lowest mapping work, weaker match to requested visual experience |

## What the source audit changed

### Existing AZ-style skin

[Marc Monka’s XDJ OPEN SOURCE](https://github.com/marcmonka/xdj-open-source-skin-mixxx/tree/9139ff1418b283c98befc90f41760dff620b2cbf)
already has the useful composition: stacked native waves, left deck metadata,
right FX panel, lower deck strips, library and setup. Its skin folder contains
a GPL v3 licence, so this project includes the credited editable adaptation.
The upstream screenshots are references; this repository’s `mixxx-*-runtime.png`
files are new captures from a running native Mixxx process.

The old VirtualDJ illustrative waveforms are not validation of this route.
The Mixxx captures use actual analysed generated calibration WAVs. Their repetitive
shape comes from that test audio. These WAVs are not shipped in the production skin.

### Loui mapping: useful research, unsuitable unchanged as this baseline

Audited [Loui1979/MIXXX-FLX10](https://github.com/Loui1979/MIXXX-FLX10/tree/4fe336a5bc4ff608e8e7578c94a78571d697c09d),
commit `4fe336a5bc4ff608e8e7578c94a78571d697c09d`.
Its controller XML has **238 input entries and 13 reused MIDI addresses**.
For example, deck SYNC at `90:58` has three entries including `sync_enabled`
and `sync_key`; `B0:13` is assigned both channel volume and quick-effect mix.
The same patterns repeat on the other decks. These are source conflicts, not
claims about a physical test or proof that the whole repository cannot work.
See the [machine-readable audit](research/loui-midi-audit.json).

The script also defaults its HID-daemon IPC and rekordbox SysEx experiment on.
The separate Linux relay README says its USB ownership makes the sound card
unavailable while relay audio remains unfinished. That relay is not required
for ordinary MIDI. Mixing those experiments into the first Windows setup adds
work unrelated to the Surface display.

### Selected mapping: the explicitly separate MIDI-only folder

Audited [Veezuhz’s MIDI-only folder](https://github.com/Veezuhz/Mixxx_FLX10_Controller_Mapping/tree/c668a0b0aa3d1230e19806380f1a711ea7a0f271/NON-HID%20FLX10%20Controller%20(working)(most%20stable)),
commit `c668a0b0aa3d1230e19806380f1a711ea7a0f271`.
It has **439 input entries, no duplicate addresses, and no missing functions
among its 25 distinct XML script bindings**. Beat SYNC uses note `0x58` and
key sync uses separate note `0x65`. Channel faders use their own volume bindings.
Its MIDI script has no SysEx handshake. These facts favour it as the first
baseline; they do not certify its scratch feel, FX behaviour or LED feedback.
See the [audit](research/veezuhz-midi-only-audit.json).

The repository root has newer HID screen work, so an unpinned “download latest”
recipe could silently change what is installed. This installer instead pins the
MIDI-only folder and both file hashes. No screen daemon, USB unlock tool, custom
Mixxx binary or replacement common-controller script is installed.

A Node VM check exercised its init and all four pitch-fader endpoints with stub
APIs. Physical MIDI delivery and real Mixxx script instantiation on Windows remain
unverified. The upstream [mapping PR](https://github.com/mixxxdj/mixxx/pull/16539)
is still a PR, not evidence that this controller mapping ships in stable Mixxx.

## USB is the main compatibility gate

The [Mixxx 2.5 manual](https://manual.mixxx.org/2.5/en/chapters/library.html#using-the-rekordbox-library)
describes legacy rekordbox USB reading, including grids/cues. Source tag 2.5.6
has `PIONEER/rekordbox/export.pdb` in
[`rekordboxfeature.cpp`](https://github.com/mixxxdj/mixxx/blob/2.5.6/src/library/rekordbox/rekordboxfeature.cpp).
[OneLibrary issue #15556](https://github.com/mixxxdj/mixxx/issues/15556) remains open.
Reading the audio files through Computer is not the same as importing that database.

The project’s read-only PowerShell check distinguishes legacy, OneLibrary and
both-file exports. It does not decrypt, convert, export, or change a drive.
The user’s export type is unknown, so the instructions assume a cloned test USB.

## Other primary sources checked

- [Mixxx current downloads](https://mixxx.org/download/): stable 2.5.6 is separate
  from 2.6 beta and 2.7 development builds. Avoid requiring nightlies for this display.
- [VirtualDJ FLX10 setup/licensing](https://virtualdj.com/manuals/hardware/pioneer/ddjflx10/setup.html):
  factory mapping/audio and Pro requirement. Its audio screenshot documents
  main channels 1–2 and headphones 3–4; these are a Windows Mixxx starting point,
  not a completed physical audio test.
- [djay Windows release notes](https://www.algoriddim.com/djay-pro-windows/releasenotes):
  FLX10 support including displays from 5.4.
- [djay Windows OneLibrary manual](https://help.algoriddim.com/user-manual/djay-pro-windows/music-library/advanced/onelibrary):
  native OneLibrary workflow.
- [djay Hardware Mode](https://community.algoriddim.com/t/hardware-mode-on-macos-and-windows/34926)
  and [customisation discussion](https://community.algoriddim.com/t/how-to-customize-the-tag-sections-in-the-pro-view-mode/32192):
  useful built-in layout, not a general custom-skin system.
- [Serato FLX10 hardware page](https://serato.com/dj/hardware/pioneer-ddj-flx10)
  and [rekordbox FAQ](https://rekordbox.com/en/support/faq/v7/): core hardware unlock.
- [Touchy WIP thread](https://virtualdj.com/forums/269853/VirtualDJ_Skins/%5BWIP%5D_Touchy_-_touch-first_skin_family_%28CDJ_%2F_XDJ-style%29_for_touchscreens.html):
  the intended VirtualDJ reference still does not provide a public downloadable
  skin ZIP in the inspected thread. No author was contacted.
