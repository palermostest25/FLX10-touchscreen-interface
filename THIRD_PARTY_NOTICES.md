# Component licences and source notices

This repository aggregates separately licensed components. The root MIT licence
does not relicense third-party skin source/assets or downloaded controller files.

| Component | Terms and source |
|---|---|
| Original AZ Touch utilities, VirtualDJ candidate and project documentation | MIT; copyright 2026 AZ Touch contributors. See [LICENSE](LICENSE). Existing exclusions for vendor software, trademarks, linked material and the supplied handoff remain. |
| Mixxx AZ Touch skin, including its upstream assets and modifications | GNU GPL version 3, as included in [the skin licence](mixxx/AZ%20Touch/LICENSE). Derived from Marc Monka's [XDJ OPEN SOURCE](https://github.com/marcmonka/xdj-open-source-skin-mixxx/tree/9139ff1418b283c98befc90f41760dff620b2cbf), commit `9139ff1418b283c98befc90f41760dff620b2cbf`. |
| FLX10 controller mapping | Separately downloaded from [Veezuhz's MIDI-only folder](https://github.com/Veezuhz/Mixxx_FLX10_Controller_Mapping/tree/c668a0b0aa3d1230e19806380f1a711ea7a0f271/NON-HID%20FLX10%20Controller%20(working)(most%20stable)), commit `c668a0b0aa3d1230e19806380f1a711ea7a0f271`; upstream terms apply. Mapping files are not redistributed here or in the skin ZIP. [The lock file](mixxx/controller-sources.lock.json) records exact URLs and hashes. |

The Mixxx adaptation was modified on **2026-10-15** by AZ Touch contributors.
[UPSTREAM.md](mixxx/UPSTREAM.md) records changes, including the Surface layout,
native waveform colours/protection, guarded loads, four labelled summaries,
mini title headers, navigation text sizing and active-view button correction.
The skin folder also carries its dated `MODIFICATIONS.md`.

The preferred editable Mixxx skin source is [mixxx/AZ Touch](mixxx/AZ%20Touch/),
also published in the [project repository](https://github.com/palermostest25/FLX10-touchscreen-interface).
`python tools/build_mixxx_skin.py` packages that folder with its GPL licence and
modification notice. Keep those notices and the applicable licence when sharing
the skin. No Mixxx/VirtualDJ binaries, device drivers or vendor trademarks are
licensed by this project; no AlphaTheta/Pioneer endorsement is implied.
