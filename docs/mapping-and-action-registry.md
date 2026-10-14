# Mapping and action registry

**Documentation inspected; host execution NOT RUN.** “Documented” below means
the official SDK/verb reference contains the element/action. It does not mean
the complete generated skin passed the installed VirtualDJ parser or hardware.
All runtime screenshots and VirtualDJ build fields remain empty.

Every dynamic expression/action occurrence is recorded with its deck/page/element
in generated [bindings.json](bindings.json). This ledger is regenerated from the
same XML tree as the package; `runtime_evidence` is NOT RUN for every row.

## Displayed deck properties

All deck rows/status strips use explicit `<deck deck="1|2|3|4">` containers;
there is no assumed correspondence between a physical side and mixer position.

| Display/property | SDK/VDJScript implementation | Unit | False/empty behavior | Official source | Runtime proof |
|---|---|---|---|---|---|
| Deck identity | `<deck deck="N">`, static label N | Logical deck | Always identifies that deck | Skin Deck | NOT RUN |
| Loaded state | `loaded`, `not loaded` visibility | Boolean | EMPTY/NO TRACK LOADED; metadata hidden | Verb list: Load | NOT RUN |
| Title | Text `action="get_title"` (scrolling performance titles) | Host string | Empty when title unavailable; unloaded fallback separately shown | Verb list: Get | NOT RUN |
| Artist | `get_artist` | Host string | Empty if unavailable | Verb list: Get | NOT RUN |
| Remaining/elapsed | `get_time 'short'`; strip `get_time 'remain' 'short'` | Formatted time | Host-defined zero/empty when unloaded | Verb list: Get | NOT RUN |
| Time mode | `display_time 'remain' ? display_time 'elapsed' : display_time 'remain'` | Display preference | Remain/elapsed label uses query; time changes only | Verb list: Hardware/display_time | NOT RUN |
| BPM | `get_bpm` | Beats/min | Hidden when unloaded; unknown remains host-defined | Verb list: Get | NOT RUN |
| Pitch | `format="%pitch"` | Percent | Hidden when unloaded | Skin Textzone | NOT RUN |
| Key | `get_key 'musical'` in performance; `get_key 'harmonic'` in browse strips | Host key string | Hidden when unloaded; unknown remains host-defined | Verb list: Key | NOT RUN |
| Scrolling waveform | `<scratchwave orientation="horizontal">` + native grid/cue | Audio/beat position | Host draws blank when unloaded | Skin Scratchwave | NOT RUN |
| Overview/progress/cue markers | `<songpos>` + `<cues>` with original PNG marker sprite | Relative audio position / POIs | Blank when unloaded; markers only when host provides them | Skin Songpos | NOT RUN |
| Cue slots 1–8 | `has_cue N`, `format="%namecueN"` | Host cue name | A–H dash fallback for absent slots; slot colors don't certify imported color fidelity | Verb list: Cue / Skin Textzone | NOT RUN |
| Playing state | `play` / `loaded & not play` visibility | Boolean | STOPPED or empty; this is transport, not “on air” | Verb list: Play | NOT RUN |
| Loop | `loop` visibility | Boolean | Indicator hidden | Verb list: Loop | NOT RUN |
| Quantize loop / setcue | `quantize_loop`, `quantize_setcue` | Independent booleans | Corresponding indicator hidden | Verb list: Config | NOT RUN |
| Sync / master | `is_sync`, `masterdeck` visibility | Native Boolean feedback | Hidden when false; sync checks BPM/phase when playing and BPM when stopped | Verb list: Sync / Deck select | NOT RUN |
| Current source path | `get_browsed_folder_path`; per-wave `get_filepath` | Native folder/file path | Host empty for pathless/virtual sources | Verb list: Get | NOT RUN |
| Clock | `format="%hour"` | Local host HH:MM | Host clock | Skin Textzone | NOT RUN |

Original BPM is documented as `get_bpm absolute` but omitted to keep this
candidate readable. On-air, Slip, FX/stems state, artwork, track
preview and original rekordbox-only tags are not released UI properties.

## Touch actions and state

| Control | Action / query | Scope and safety | Runtime proof |
|---|---|---|---|
| Source/Browse/Playlist/Tag/Search/Waveform | `skin_panel 'name' on`; query `skin_panel 'name'` | Panels use one `az-pages` group; query highlights the active page. Audio untouched. | NOT RUN |
| Source / Playlist | Above plus `browser_window 'folders'` | Focus native folder navigator; select actual USB/list manually. | NOT RUN |
| Tag | Above plus `browser_window 'sidelist'` | Native `filelist source="sidelist"`; does not claim Pioneer tag interoperability. | NOT RUN |
| Search / Keyboard | `search & show_keyboard` | Native keyboard request/search focus; automatic Windows keyboard not assumed. | NOT RUN |
| Four/two deck view | `skin_panel 'four|two12|two34' on` | One `az-performance` group; display visibility only. | NOT RUN |
| AZ Colors | `setting 'skinWaveformType' 'shapes' & setting 'skinOverviewType' 'shapes'` | Explicit display preset; blue/orange/ivory native stem components, no audio command. | NOT RUN |
| Frequency Colors | `setting 'skinWaveformType' 'colors' & setting 'skinOverviewType' 'colors' & setting 'waveUseFrequency' on` | Explicit native frequency color mode; host owns palette. | NOT RUN |
| Zoom | `zoom -0.05`, `zoom +0.05` | Shared visualization zoom, not pitch/seek. | NOT RUN |
| Load N | `deck N play ? nothing : deck N load`; query `deck N play` | Guard and target are same explicit deck; red PLAYING/LOCKED label. No live-load override. | NOT RUN |
| Parent | `browser_window 'folders' & browser_scroll 'parent'` | Native folder navigation only. | NOT RUN |
| Add to Tag | `browser_window 'songs' & sidelist_add` | Focuses songs and adds native selected file(s) to local sidelist. Selection focus must be tested. | NOT RUN |
| Settings | `settings` | Host configuration dialog. | NOT RUN |
| Fullscreen | `maximize` | Host documented window-mode cycle. | NOT RUN |
| Waveform/overview shield | `<button action="nothing" rightclick="nothing" middleclick="nothing" dblclick="nothing">` + explicit `<mouserect>` | Later sibling covers renderer exactly; transparent off graphic. Permanent shield, paused or playing. Static coverage passes; actual input dispatch unproven. | NOT RUN |
| Startup | `skin_panel 'waveform' on & skin_panel 'two12' on` | Display panels only, no audio/settings write. | NOT RUN |

SDK sources for the above are linked in [sdk-references.md](sdk-references.md).
The validator limits oninit to panel selection, rejects unguarded/mismatched
loads, requires renderer shields, checks named references and canvas bounds.
There is no official offline XSD included; project lint cannot replace host
parser validation.

## FLX10 mapping contract

**Files changed: none.** Use the official factory default device definition and
mapper. This repository does not distribute a renamed/default/custom mapper.
Hardware LOAD protection must be separately checked under the host's loadSecurity
option. Native browser double-click/drag-and-drop is likewise not intercepted.

Left physical side: deck 1 ↔ 3. Right physical side: deck 2 ↔ 4. Verify the
four mixer channels, outputs and headphone PFL audibly. Also check jog displays,
PLAY/CUE, pitch, encoder/select/load, pads, loops, Beat FX and track separation
against the [hardware manual](https://virtualdj.com/manuals/hardware/pioneer/ddjflx10.html).
If a conflict is reproduced, back up/export the original mapper and document
only the necessary change; do not remap blindly.
