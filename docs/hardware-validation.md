# Surface / FLX10 validation handoff

G0–G5 are **BLOCKED: target equipment and software are not attached**. The
candidate package is shipped under the brief's explicit no-physical-access
exception. No physical capability has been marked PASS.

## Environment facts

| Fact | Actual observation |
|---|---|
| Build host | Linux cloud workspace; no target hardware |
| Target | User-specified Surface Pro 7, Windows, 2736 × 1824, 3:2 |
| Windows version | UNKNOWN — record on Surface |
| Surface CPU/RAM/GPU | UNKNOWN — record on Surface |
| VirtualDJ installed/tested build | NONE in build workspace / UNKNOWN on Surface |
| Licence entitlement | UNKNOWN — check Pro Infinity/Subscription; do not purchase without user instruction |
| FLX10 driver/firmware | UNKNOWN |
| Factory mapping version | UNKNOWN; no mapping files changed by this project |
| Audio preset/routes/sample rate/buffer | UNKNOWN; use official native FLX10 setup |
| Display scaling/touch behavior | NOT RUN; start with native resolution and test 200% |
| Backup paths on Surface | NOT CREATED here; run backup/manual snapshot before testing |
| USB filesystem/export type | UNKNOWN; clone and record OneLibrary vs legacy vs dual export |

## Gates, in order

| Gate | Current state | Procedure / evidence required |
|---|---|---|
| G0 FLX10 + native audio | BLOCKED | Stock UI recognizes device; audibly test four decks and Master/PFL. Record driver/firmware/mapper/audio setup screenshots. |
| G1 licence | BLOCKED | Confirm actual FLX10 entitlement in host; record status, without exposing account credentials. |
| G2 USB read | BLOCKED | Clone original; prove real OneLibrary playlists and USB paths. Test export types separately in stock UI. |
| G3 cue/grid fidelity | BLOCKED | Compare ten tracks against export using the compatibility report. |
| G4 skin SDK | BLOCKED (structural package checks PASS) | Extract current shipped/default skin for build-specific comparison. Install spike; capture live deck labels, moving waveform, native USB browser and page/load touch actions. |
| G5 Surface touch | BLOCKED | Actual taps/scroll/keyboard/hit shields at native resolution and tested DPI values. |

Do not continue to stage use when a gate fails. Packaging and source work can
proceed, but neither substitutes for gate evidence.

## Run sequence

1. Follow README prerequisites/backups and prepare cloned media. Keep original detached.
2. Prove stock host G0/G1, then stock browser G2/G3; fill exact source/version results.
3. Extract the installed default skin via Settings → Interface and compare SDK
   idioms to the candidate. Install the spike. Record G4 evidence before main UI.
4. Install main skin; test stopped load, active load blocking on all four decks,
   cue labels/positions and pitch/key/time changes using hardware controls.
5. Before any performance test, attempt all T07 input gestures on waveform and
   overview. If transport moves, return to stock skin and report the failure.
6. Execute [T01–T20](../tests/smoke-checklist.md). Use [test-results](../tests/test-results.md)
   for statuses, UTC time, exact versions and evidence links. Never promote a
   blocked/not-run check to PASS based only on documentation.
7. Capture real screenshots at 2736 × 1824: four decks, two decks, Browse on
   actual USB, Source tree and host Settings/audio. Name files as described in
   [screenshots/README.md](screenshots/README.md). No FX screenshot until implemented.
8. Record performance and persistence; prove rollback and original USB safety.

## Scaling matrix

| Resolution | Windows scale | Window mode | Touch alignment | Cropping/readability | Result |
|---|---|---|---|---|---|
| 2736 × 1824 | 150% | Fullscreen/windowed | — | — | NOT RUN |
| 2736 × 1824 | 175% | Fullscreen/windowed | — | — | NOT RUN |
| 2736 × 1824 | 200% | Fullscreen/windowed | — | — | NOT RUN |

Measure physical button size (target around 9 mm) on the actual display, not
from XML pixel counts. Minimum custom interactive height is 52 design pixels;
native browser hit targets remain host-controlled.

## Performance and offline record

| Scenario | CPU/memory | Startup/browse time | Audio meter/dropouts | Result |
|---|---|---|---|---|
| Stock UI, two decks | — | — | — | NOT RUN |
| AZ Touch, two decks | — | — | — | NOT RUN |
| AZ Touch, four decks, cloned USB | — | — | — | NOT RUN |
| 60-minute four-deck session | — | — | — | NOT RUN |
| Wi-Fi off, valid cached entitlement | — | — | — | NOT RUN |

Use the same driver/buffer/audio settings for comparisons. Do not assert FPS or
latency without measurement. USB errors are host feedback; verify other decks
survive disconnect and do not enable automatic destructive rescans.

## Blocker report template

```text
Gate/test:
UTC timestamp:
Windows / VirtualDJ build / driver / firmware / mapping:
USB filesystem / rekordbox version / export type:
Command or exact touch/hardware action:
Observed behavior and reproduction steps:
Screenshot/log path:
Stock skin comparison:
Official documentation or SDK limitation (if known):
Required next action:
```

Missing hardware/runtime evidence cannot be solved by a skin helper/plugin. No
plugin is proposed. If an actual SDK limitation is reproduced, first identify
a documented supported API and necessary changes before considering an extension.
