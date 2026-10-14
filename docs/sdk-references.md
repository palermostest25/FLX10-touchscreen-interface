# Official references checked during implementation

Retrieved 2026-10-14. Documentation presence is distinguished from runtime proof.
No third-party skin code or product bitmaps are included in the package.

| Reference | Used for |
|---|---|
| [Skin SDK](https://virtualdj.com/wiki/Skin%20SDK) | SDK 8 root attributes, flat XML/PNG ZIP and optional actual-screenshot preview |
| [Deck](https://virtualdj.com/wiki/Skin%20Deck.html) | Explicit 1–4 context inheritance |
| [Panel](https://virtualdj.com/wiki/Skin%20SDK%20Panel.html) | Named groups, initial visibility and panel switching |
| [Button](https://virtualdj.com/wiki/Skin%20Button.html) | Vector off/down/selected graphics, textselected, actions/query, mouserect/no-op shields |
| [Textzone](https://virtualdj.com/wiki/Skin%20SDK%20Textzone.html) | Text action getters, %pitch, %hour and font/position syntax |
| [Scratchwave](https://virtualdj.com/wiki/Skin%20Scratchwave.html) | Native moving waveform, grid and cue mask/text |
| [Songpos](https://virtualdj.com/wiki/Skin%20songpos.html) | Overview and original cue-marker sprite |
| [Browser](https://virtualdj.com/wiki/skinbrowser.html) | Native browser attributes/colors/font/lineheight |
| [Custom Browser](https://virtualdj.com/wiki/Custom-Browser.html) | filelist source=sidelist and native layout boundaries |
| [Official SDK browser example](https://virtualdj.com/files/SDK%20Example%20-%20Custom%20Browser%20Skin.zip) | Inspected actual published XML for containers, native waveform and sprite patterns; not copied into distribution |
| [Draw shapes](https://virtualdj.com/wiki/Skin%20Draws.html) | Original rectangles and ARGB/color syntax |
| [Common attributes](https://virtualdj.com/wiki/Skin%20Element%20Properties.html) | Deck and VDJScript visibility |
| [OnInit](https://virtualdj.com/wiki/Skin%20OnInit.html) | Startup panel action |
| [VDJScript verbs](https://virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) | All emitted actions/getters/queries and flow syntax |
| [Options list](https://virtualdj.com/manuals/virtualdj/appendix/optionslist.html) | readOnly, loadSecurity, touch/keyboard and performance options |
| [FLX10 setup](https://virtualdj.com/manuals/hardware/pioneer/ddjflx10/setup.html) | Pro licence, native audio preset, driver and factory mapping |
| [OneLibrary](https://virtualdj.com/manuals/virtualdj/interface/database/cdjexport.html) | Native export/browser workflow and sync options, not proof of import |
| [rekordbox OneLibrary FAQ](https://rekordbox.com/en/support/faq/onelibrary-7/) | Format/dual-library distinction; clone-only fallback evaluation |

Concept brief: the user's attached *Touchscreen_AZ_Agent_Handoff.html*, preserved
as [handoff.html](handoff.html). Visual inspiration is acknowledged to the
[Touchy AZ WIP discussion](https://virtualdj.com/forums/269853/VirtualDJ_Skins/%5BWIP%5D_Touchy_-_touch-first_skin_family_%28CDJ_%2F_XDJ-style%29_for_touchscreens.html).
No Touchy code/assets were downloaded or reused; availability/public release is
not assumed. The graphic atlas is drawn by this repository's own generator.

0.3.0 additional sources: [waveform manual](https://virtualdj.com/manuals/virtualdj/interface/topsection/appcontrols/layout/waveform.html)
and [documented palette example](https://virtualdj.com/forums/270039/VirtualDJ_Skins/Rekordbox_3_Band_color_waveform_XLM_edit_help..html).
Native waveform overlay structure was compared with the official SDK browser
example. Shapes/frequency rendering remains distinct; see waveform-modes.md.
