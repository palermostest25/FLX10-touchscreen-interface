# AZ Touch — FLX10 touchscreen interface

A native **VirtualDJ XML + PNG skin** for a Surface Pro 7 and DDJ-FLX10. The
Surface provides a 3:2 player display; VirtualDJ handles audio and libraries;
the FLX10 remains the mixer and transport controller.

**Status: 0.2.0 hardware validation candidate.** The archives are built and
structurally checked. They have **not been loaded in VirtualDJ** here. Surface
touch, FLX10 audio/mapping, licensing, and rekordbox OneLibrary import are
**NOT RUN**. This is a usable installation/test milestone, not a verified stage
release. Complete the [hardware checklist](docs/hardware-validation.md) before
using it at a gig. No simulated audio engine or fabricated USB results are included.

The performance layout now follows the **Touchy AZ screenshot linked in the
handoff**: black canvas, large stacked waveforms at the top, a central cue bank,
and four larger player displays in a 2×2 grid below. The earlier generic row-card
layout has been replaced. This is an independent implementation of the visual
structure, not the original Touchy skin. The linked author thread provides
screenshots but no downloadable skin ZIP as checked on 14 October 2026.

[Inspect the empty-state layout diagram](docs/screenshots/layout-reference-structure.png)
(offline geometry rendering, **not** a VirtualDJ runtime screenshot).

## What is included

- Four live native scratch waveforms, track overview waveforms, cue markers,
  track titles/artists, BPM, pitch, harmonic key, remaining/elapsed time, and
  playing/loop/quantize indicators, all bound to VirtualDJ's decks.
- Four-deck view and larger two-deck views for 1+2 or 3+4; four-deck status on
  every main page. No onscreen jog wheels, mixer faders, or EQs.
- Source, Browse, Playlist, Search and local VirtualDJ Sidelist/Tag List pages
  using the native browser. Source shows the actual selected folder path.
- Explicit LOAD 1–4 buttons that issue `load` only when that deck is not playing.
  Waveform hit shields are designed to consume touch input at all times.
- Settings, fullscreen, touch keyboard access, deterministic packages, installer,
  backup and rollback tools. No custom controller mapping is installed.

These describe implemented bindings; correct runtime behavior still needs testing.
Optional FX, prelisten, USB-disconnect banners, touch-triggered cues and paused
seeking are omitted. See [limitations](docs/known-limitations.md).

## 1. Install prerequisites on the Surface

1. Install an up-to-date Windows build of [VirtualDJ](https://virtualdj.com/download/).
   Open it once, sign in, then close it. Record its build number in the hardware report.
2. For sustained FLX10 control, verify **Pro Infinity or Pro Subscription** on
   your account. The [official setup guide](https://virtualdj.com/manuals/hardware/pioneer/ddjflx10/setup.html)
   says operation without these is limited to ten minutes per launch. This
   project does not include VirtualDJ, a licence, or the FLX10 Windows driver.
3. Install the current **DDJ-FLX10 Windows audio driver** from
   [AlphaTheta/Pioneer DJ support](https://www.pioneerdj.com/en/support/software/controller/ddj-flx10/).
   Check firmware against the official support page; follow the vendor's update
   procedure if an update is needed. Connect power and USB directly where possible.
4. Use landscape, **2736 × 1824** resolution. Start at Windows **200%** scaling
   (the skin's design canvas is 1368 × 912), then test fullscreen and touch
   alignment. 150% and 175% are test cases, not certified combinations.
5. Keep the original rekordbox USB detached. Make a separate **cloned test drive**
   or export a duplicate test USB. Record rekordbox version, filesystem and
   export type: OneLibrary only, legacy Device Library, or both.

## 2. Download the project

On [the repository page](https://github.com/palermostest25/FLX10-touchscreen-interface),
choose **Code → Download ZIP**, extract the whole download to a local folder
(for example `Downloads\FLX10-touchscreen-interface-main`), and open that folder.

Use **`dist\AZ-Touch-3x2.zip`** as the skin. Keep this inner ZIP **zipped**.
The outer GitHub source ZIP is not a VirtualDJ skin. Python is not required to
install the prebuilt skin.

## 3. Find your VirtualDJ home and make a backup

In VirtualDJ Settings → Options, search for **home folder** and use the folder
button if offered by your build. Otherwise find the active folder containing
`settings.xml`, `Skins` and your databases. Common locations include:

- `%LOCALAPPDATA%\VirtualDJ`
- `%USERPROFILE%\Documents\VirtualDJ` (possibly redirected to OneDrive)

Close VirtualDJ. Back up `settings.xml`, `database.xml`, `Mappers`, `Devices`,
`Skins`, `Playlists`, `Folders` and `History` from that home folder. Back up any
external-drive databases separately. Do not overwrite them during installation.

The optional script below snapshots those local items into
`<VirtualDJ home>\AZTouch-backups\<timestamp-id>`. It does not clone your USB
or music files. Save the backup path it prints.

Open **Windows PowerShell as your normal user**, change to the extracted project,
and run (replace the sample path with your actual home):

```powershell
cd "$env:USERPROFILE\Downloads\FLX10-touchscreen-interface-main"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\backup_windows.ps1 -VirtualDJHome "$env:LOCALAPPDATA\VirtualDJ"
```

`-ExecutionPolicy Bypass` applies only to that process. If your organisation
blocks scripts, use the manual installation below. No administrator session or
system-wide execution policy change is needed.

## 4. Install the skin

### Manual installation

1. Close VirtualDJ.
2. Copy `dist\AZ-Touch-3x2.zip` into `<VirtualDJ home>\Skins\`.
3. If that filename already exists, copy the old file somewhere safe first.
   Replace only this AZ Touch file; leave other skins/settings/mappers alone.
4. Start VirtualDJ, open **Settings → Interface**, and select
   **AZ Touch 3x2 · Hardware candidate**.

### Scripted installation

From the project directory:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_windows.ps1 -VirtualDJHome "$env:LOCALAPPDATA\VirtualDJ"
```

You can omit `-VirtualDJHome` if exactly one supported home is detected. If
multiple homes are present, the script refuses to guess. It checks
`dist\SHA256SUMS.txt`, verifies the archive entries, copies the skin and prints
an **install receipt path**. Save that path for rollback. It refuses to run
while VirtualDJ is open. Existing AZ Touch packages require the explicit
`-Replace` flag and are backed up first.

Add `-WhatIf` to preview file changes. The installer never edits `settings.xml`,
controller mappings, databases, USBs, audio routing or Windows registry settings.

For a smaller first SDK test, install `dist\AZ-Touch-SDK-Spike.zip` instead:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\install_windows.ps1 -VirtualDJHome "$env:LOCALAPPDATA\VirtualDJ" -SkinZip .\dist\AZ-Touch-SDK-Spike.zip
```

Select **AZ Touch SDK spike · Hardware candidate** in Settings → Interface.
Prove its live deck text, moving waveform, native browser and page switching
before testing the main skin. The spike has two display rows and four guarded
load buttons; it still declares four VirtualDJ decks.

## 5. Set up and prove the FLX10 in the stock skin first

1. Power on the FLX10, attach headphones to it, connect speakers to its Master
   output, and connect its USB port to the Surface.
2. Start VirtualDJ using its stock skin first. Accept the **DDJ-FLX10 audio
   preset** when prompted, or select it in **Settings → Audio**. Follow the
   [official FLX10 setup guide](https://virtualdj.com/manuals/hardware/pioneer/ddjflx10/setup.html);
   use the installed native driver/preset rather than guessed channel numbers.
3. In **Settings → Controllers/Mappings** (label depends on build), choose the
   FLX10 **factory default** mapping. AZ Touch does not require a custom mapper.
4. Load a local test track on each of four decks. Confirm audible Master output,
   individual headphone PFL, faders, pitch, PLAY/CUE, jogs and pads on each deck.
5. The left FLX10 deck side selects **1 or 3**; the right selects **2 or 4**.
   Check both hardware layer switches. Verify mixer channel routes audibly;
   physical left/right does not by itself identify every mixer channel.
6. Record actual sample rate, buffer, driver, firmware, mapping and licence.
   If stock VirtualDJ cannot pass, fix that before testing this skin.

## 6. Protect the test USB and verify its library

In stock VirtualDJ, before inserting the cloned USB:

1. In Settings → Options, set **`readOnly`** on for this test. The official
   option prevents drive database modification; it is **not an OS-level write
   blocker** and does not guarantee that every feature avoids writing files.
2. Disable **Auto sync cue points** and **Auto generate stems** in the OneLibrary
   folder context menu and, once visible, the test drive's own context menu.
   Avoid export, drag-and-drop copying, creating playlists, tag edits, and
   library conversion on the USB. Use a hardware write blocker if strict
   no-write evidence is required.
3. Insert the clone. Expand **OneLibrary** in the native folder tree and choose
   the drive and a real playlist. If OneLibrary is hidden, use the native
   browser's root-folder/view options. Do not click an empty-drive prompt to
   create a database on a source drive.
4. Confirm the physical file paths are on the USB; load and play real tracks.
   Compare at least ten tracks' BPM/key, grids, hot cues, memory cues, names
   and artwork to the rekordbox export. Fill in the
   [compatibility report](docs/source-compatibility.md).
5. **If only plain audio folders or the legacy Device Library works, OneLibrary
   import is not proven.** Record the failure. Dual-format export on a duplicate
   USB is an explicit fallback to evaluate, not a hidden substitute for passing
   OneLibrary. The skin cannot repair a VirtualDJ library reader limitation.

The [VirtualDJ OneLibrary manual](https://virtualdj.com/manuals/virtualdj/interface/database/cdjexport.html)
documents export and sync features; that alone does not prove exact import
compatibility with your rekordbox USB.

## 7. Use AZ Touch

- **WAVEFORM** returns to the player screen from any main page. Choose **4 DECK**,
  **2 DECK / 1 + 2**, or **2 DECK / 3 + 4**. The lower four-deck player grid remains.
  Tap a waveform's deck number to change the sidebar display; this changes only
  displayed metadata and does not select an audio deck or change headphone PFL.
- **SOURCE** exposes the native tree. Expand OneLibrary → USB → playlist.
  Local storage and local rekordbox collections are whatever the actual native
  tree exposes; the skin does not invent drive tiles or copy music.
- **BROWSE / PLAYLIST** share the native library browser. Playlist focuses the
  folder tree; select the intended list there. Configure columns using the
  native header menu: Title, Artist, BPM, Key and Length as available. Large
  row spacing is requested by the skin; adjust native font size if necessary.
- Tap a song once, then use **LOAD 1–4** for the intended stopped deck. A playing
  target shows **PLAYING / LOCKED** and the touch action does nothing. To replace
  it deliberately, stop that deck using the FLX10, verify it is stopped, then
  load. The skin offers no live-load override.
- In Settings → Options, enable **`loadSecurity`** using the confirmation/silent
  protection choice your build offers. This is separately needed for native
  browser double-click/drag-and-drop and factory hardware LOAD actions, which
  are outside the skin buttons. Test all routes; do not assume a guard applies
  globally just because a touch button is guarded.
- **SEARCH / KEYBOARD** focuses the real search field and requests VirtualDJ's
  onscreen keyboard. Enable **`onScreenKeyboard`** in Options if necessary.
  Windows' taskbar Touch keyboard is an alternative. Test with the Type Cover
  folded away; automatic Windows keyboard invocation is not certified here.
- **TAG LIST** shows the local VirtualDJ **Sidelist**. Select a track in Browse,
  use **ADD TO TAG**, then switch to Tag List. Verify focused selection behavior
  on your build. This is not the Pioneer USB Tag List format.
- Tap a deck's time display to switch remaining/elapsed. PLAYING, LOOP, Q LOOP
  and Q CUE are passive indicators. Cue labels are passive too; use FLX10 pads.
- Waveforms and track overviews are display-only, including while paused.
  **Confirm T07 touch/drag safety before relying on the hit shields.**
- **FULLSCREEN** cycles the host window modes; **SETTINGS** opens VirtualDJ
  configuration. Exit using VirtualDJ/Windows' normal close path after your set.

Navigation changes page visibility only. It does not switch the audio preset,
move faders, trigger effects or reset decks. Startup explicitly selects the
four-deck Waveform page. Other preferences are saved by VirtualDJ as supported.

## 8. Roll back or uninstall

1. In VirtualDJ **Settings → Interface**, select your previous/default skin.
2. Close VirtualDJ.
3. For a manual install, remove only `Skins\AZ-Touch-3x2.zip` (and the optional
   spike ZIP), or replace it with the copy you saved before installing.
4. For a scripted install, use the **matching receipt** printed during installation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\restore_default.ps1 -ReceiptPath "C:\actual\VirtualDJ\AZTouch-backups\timestamp-id\install-receipt.json"
```

The rollback script verifies that AZ Touch has not changed since installation,
then removes it or restores its backed-up package. It refuses to delete a
different version. It leaves settings/mappings/databases alone and does not
automatically edit VirtualDJ's selected skin. For a spike install, use its own
receipt. Restore older replacements in reverse installation order.

## Troubleshooting

| Problem | Action |
|---|---|
| Skin absent from Interface | Check the actual active home folder, inner ZIP, flat XML/PNG entries, and restart VirtualDJ. |
| XML/load/render error | Return to the stock skin; record build, error and screenshot. Test the SDK spike and report the exact failure. Structural lint cannot prove the host accepts it. |
| No audio/PFL | Test the stock skin and official FLX10 preset/driver first; inspect licence and factory mapping. |
| Missing USB playlists | Check export format, actual drive paths, build and OneLibrary tree options. Do not convert the original drive. |
| Touch seeks or scratches | Stop testing this skin, restore stock UI, report T07 failure. The input shield requires target validation. |
| Touch keyboard does not appear | Enable onScreenKeyboard, use KEYBOARD, or use Windows taskbar Touch keyboard; record T10 result. |
| Cropped/offset controls | Set native 3:2 resolution; test fullscreen at 200%, then compare the scaling matrix. |
| Audio pops/high CPU | Record stock vs AZ Touch CPU/audio meters with identical buffers; lower native skinFPS if appropriate. Avoid realtime high-quality stems on an untested Surface. |
| Replacement/rollback refused | Use -Replace for an intended skin update, or the matching receipt for rollback. Do not delete unrelated files. |

## Build from source (developers only)

Python **3.10+** and Pillow are required for generation/validation. Windows example:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools\build_skin.py
.\.venv\Scripts\python.exe tools\validate_skin.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On Linux/macOS, use `python3 -m venv .venv` and `.venv/bin/python` for the same
commands. These platforms build artifacts; playback targets Windows VirtualDJ.
ZIP timestamps/order are fixed, compression is stored, and SHA-256 checksums
are regenerated in `dist\SHA256SUMS.txt`. The validator checks this project's
vocabulary, geometry, references and guards; it is **not an official SDK schema**.
Generator code is the source of truth; rebuilding overwrites generated XML/PNG
and the binding ledger.

See [action registry](docs/mapping-and-action-registry.md),
[test results](tests/test-results.md), [SDK references](docs/sdk-references.md),
and [changelog](CHANGELOG.md). Original code/graphics are MIT licensed; no
VirtualDJ software, vendor artwork, or Touchy AZ code/assets are redistributed.
AZ Touch is independent and unaffiliated with Atomix, AlphaTheta, Pioneer DJ,
rekordbox or Kiwi Gazza.
