# Source and modification notice

AZ Touch for Mixxx is derived from Marc Monka’s
[XDJ OPEN SOURCE](https://github.com/marcmonka/xdj-open-source-skin-mixxx/tree/9139ff1418b283c98befc90f41760dff620b2cbf),
commit `9139ff1418b283c98befc90f41760dff620b2cbf`.
The upstream licence is inside `AZ Touch/LICENSE`: GNU GPL version 3.
The modified skin is supplied as editable XML/QSS and assets under that licence;
it is not covered by the repository root’s MIT licence. Original author and
upstream visual work remain credited. No AlphaTheta or Pioneer endorsement is implied.

Modified 2026-10-15 for a Surface Pro 7 / FLX10 companion display:

- Renamed manifest, Segoe UI/DejaVu font fallback and 1100 × 700 minimum area.
- Native 1+2, 3+4 and four-wave stacks with aligned metadata; four summaries on
  performance, library and setup pages regardless of waveform view.
- Frequency colours blue/orange/ivory, more visible grid lines, disabled native
  waveform input and drops, native safe-load buttons and larger view buttons.
- Corrected time visibility/sizing, explicit native play-position connections,
  invalid upstream QSS declarations and invalid VU-meter tooltip identifiers.
- Added persistent DECK 1–4/title headers to library/setup summaries, with 13px
  text in 24px rows, and corrected Browse/Back navigation labels to 14px.
- Disabled the active wave-view button so repeated taps retain the selected
  native stack page instead of toggling it off and cycling to another view.
- Kept native effects, track state, key, quantize, cue markers and recording.

The full preferred editable source is [`mixxx/AZ Touch/`](AZ%20Touch/) in the
[project repository](https://github.com/palermostest25/FLX10-touchscreen-interface).
The skin package is a ZIP of that source, including `LICENSE` and the dated
`MODIFICATIONS.md`. Build with `python tools/build_mixxx_skin.py`; no host binary
is included. See [component notices](../THIRD_PARTY_NOTICES.md) for licence scope.

Controller selection is a separate component, downloaded by the end user from
Veezuhz’s repository. The exact commit, variant, URLs and hashes are in
[`controller-sources.lock.json`](controller-sources.lock.json). Its files are not
distributed in this repository or the skin archive and retain upstream terms.
The installer only changes the local preset name and JavaScript reference to
avoid overwriting other mapping files; it does not rewrite its MIDI behaviour.
