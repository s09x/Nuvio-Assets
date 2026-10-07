# Nuvio stream badges

Release **2.0.0** contains **1,037 badges in 37 categories**: 94 original-logo assets, 892 neutral text labels, 50 static language flags and one user-approved HDR10 derivative. Every entry has a **1280 x 720 lossless WebP RGBA master**, downsampled from the approved 4K delivery artwork with Lanczos, and a smaller app image. Existing app images already fit 720p bounds and retain their exact bytes; matching rules and the import version remain unchanged.

## Import into Nuvio

Open **Settings > Streams > Stream badge URLs**, add or refresh this URL and activate the import:

```text
https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/manifest.json
```

The import URL and all 1,037 IDs remain stable. Each image URL includes a content-hash query so a refreshed import uses the revised artwork rather than an old cached frame. `2160p` remains an input alias but displays **4K**; both entries share one image URL for Nuvio deduplication. No app code was changed.

Matching uses text supplied by stream providers. It cannot infer missing metadata. All assets support explicit selectors such as `[badge:resolution/2160p]`. Ambiguous values require context: `[EN]` selects English, while `provider: EN` selects Easynews. Only the active imported source contributes badges in the inspected client.

## Approved design

Original graphics preserve their original identity, colors and proportions. Technical values without a verified exact mark use JetBrains Sans SemiBold in neutral off-white. There are **no added badge frames, outlines, shadows, metallic effects or category color accents**. Any border or background intrinsic to an original mark remains part of that mark.

The previous seven custom logo combinations are replaced by neutral labels. They are not represented as official standalone logos. AV1, Opus, DivX, FLAC, Speex and Theora now use verified upstream originals. Provenance for every delivered image is in `data/catalog.json`; original source bytes are retained.

HDR10 is the explicitly approved derivative of the supplied HDR10+ image, edited with `gpt-image-2.5-sunburst` and locally registered to preserve the unaffected original pixels. The plus is removed and the zero closed. **It is not an issuer-provided official HDR10 mark.** The native source was 831 x 179; the model output was 1672 x 941; the approved 4K source presentation export adds no claim of native 4K detail. Its approved app file is preserved byte-for-byte. The delivered master is downsampled to 1280 x 720 and encoded as lossless WebP; the approved PNG remains unchanged in `sources/approved-borderless`.

The 50 selected language flags retain the established country/region mappings and exclude India assignments. Language-code centering records refer to the original source geometry. DE and EN retain the exact approved app and source files; their delivery masters are downsampled with the rest of the library. See [language mappings](language-flags.md).

The inspected Nuvio image area is 16 dp high and 34–92 dp wide. Transparent safety padding protects logo/text ink from the client's 6 dp corner clip. App copies are at most 900 x 600 pixels. Long labels and tall original marks necessarily appear smaller in this slot. Light review backgrounds help inspect dark originals and are not baked into their transparent exteriors.

## Coverage and evidence

All **698 pinned source mappings** still resolve. The complete associated language/region/provider lists and extended media-format inventory are preserved. Coverage is tied to AIOStreams commit `f67d00ac6cd6d4efdde01f5d6f59bf1dbee95854`, `@viren070/parse-torrent-title` 0.8.8 and the previously inspected client/StreamForge contracts. Arbitrary titles, filenames, dates, sizes, counts and future user-defined values are not a finite pre-rendered set; their field-label assets are included.

The resolution-change checks decode all masters as 1280 x 720 RGBA, verify their current checksums and lossless encoding, and confirm that all app images and archived sources retain their original bytes. Each resized lossless image is compared against the Lanczos result during conversion. Original production checks verified all source mappings and all 50 flag-code centers. All 1,037 unchanged app images were previously simulated at densities 1 and 2: **2,074 layout checks**, with no opaque non-flag ink clipped. Flag field corners are intentionally clipped by the client. Historical flag-layout and publication reports apply to their recorded source geometry or earlier publication, as identified in the current verification report.

The manifest validation compiles all 1,037 expressions, verifies image paths and content versions, checks the 4K alias, and runs the synthetic import fixtures. Regex checks use .NET with the inspected shared Unicode/lookaround syntax. **No physical Nuvio device import or theme acceptance test was performed.**

## Rebuild and review

```sh
python badges/tools/render_borderless.py --font /path/to/jetbrains_sans_semibold.ttf
python badges/tools/build_manifest.py
pwsh -File badges/tools/verify_manifest.ps1
```

The renderer requires the approved font checksum recorded in the plan; font software is not redistributed. The checked-in masters and approved source seeds act as immutable image inputs. Rendering preserves source geometry and exports delivery masters at 1280 x 720. Brand sources retain their individual attribution and licensing; no blanket ownership of trademarks is claimed. `sources/type` contains the historical v1 reference only and is not the active v2 renderer. Preview sheets fit 720p bounds without upscaling or cropping.

- `manifest.json`: stable Nuvio import.
- `masters/` and `web/`: all 2,074 artwork files.
- `index.html`: offline searchable gallery with category, artwork type and 16-pixel views.
- `previews/`: every category, all 50 flags and a native-size simulation.
- `data/catalog.json`: current artwork paths, checksums, matching aliases and provenance.
- `data/verification.json`, `data/nuvio-size-checks.json`: executed artwork checks.
- `data/import-verification.json`: executed import-rule checks.
- `data/borderless-render-plan.json`: reproducible inputs and alias mapping.
- `sources/approved-borderless/`: exact approved seed artwork and HDR10 provenance.
