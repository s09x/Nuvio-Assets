# Nuvio stream badge library

User-approved asset library and Nuvio import configuration.

The collection contains **1037 badges**: 942 fixed-type badges, 88 brand-mark badges and 7 compositions. Each has a **3840 x 2160 RGBA lossless WebP master** and a separate cropped app preview. All 2,074 image paths are present and verified.

## Import into Nuvio

Open **Settings > Streams > Stream badge URLs**, add the following URL and activate that import:

```text
https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/manifest.json
```

The manifest uses Nuvio's `filters` and `groups` format, with **1,037 enabled entries in 37 groups**. `imageURL` points to the smaller `web` images for stream chips. All corresponding 4K `masters` remain available. Nuvio deduplicates images by URL; byte-identical artwork aliases therefore share a canonical app-image URL. Only the active imported source contributes matching badges in the inspected client.

Language recognition uses the selected 50 language names and aliases in language fields, lists, release metadata or flag markers. Ordinary two-letter words are not treated as free-standing language identifiers. Other languages, country labels, generic status words and ambiguous metadata require context. For example, `provider: EN` selects Easynews, while `[EN]` selects English. Every catalog item also has an unambiguous selector such as `[badge:resolution/2160p]`.

The matcher can only use text exposed by the stream provider; it cannot infer missing metadata. Its independent rules can show multiple badges when several labels are present. It does not establish decoder support, and no client code was changed. The language-to-flag mapping is documented in [language-flags.md](language-flags.md); the 50 flag language badges exclude India assignments.

[Import matching notes](data/import-matching.json) and [validation results](data/import-verification.json) record the rule scope. Validation covers the inspected JSON contract, compilation of every expression, local image paths and 20 synthetic stream cases. Regex behavior was exercised with .NET's shared Unicode/lookaround syntax; an import on a physical Nuvio device was not performed.

To rebuild and check the import:

```sh
python badges/tools/build_manifest.py
pwsh -File badges/tools/verify_manifest.ps1
```

## Approved design and reproducibility

The shared type and frame master was explicitly approved by the user. Its geometry SHA-256 is `2104dd08a14327ad320e4e32524ddf94f588ab39876fddf2caf1e536ddd69d06`. Every generated label reuses those exact character contours and spacing/frame rules. No per-label image-model drawing, substitute font or individual character stretching is used. The original visual reference was created with `gpt-image-2.5-sunburst`; production uses the approved deterministic vector master.

The baseline production renderer reproduced all 16 approved 4K examples with **zero differing RGBA pixels** before flag backgrounds were added. These comparisons cover the baseline foreground renderer. Flag-backed derivatives deliberately have different background pixels; their foreground and exterior-edge checks are recorded separately in `data/language-flag-verification.json`. The recurring-2 proof and complete character master are included in `previews`. Foreground color and material operations stay inside the fixed letter/frame alpha. The same native geometry is used for every occurrence of a character; rasterization at different scales naturally has different antialiasing samples.

50 language badges use flat flag backgrounds. The flag fills the complete badge interior; the approved lettering and frame remain above it. The exterior remains transparent. There are no fabric folds, waving effects or flag shadows. The curated 50-language selection excludes India mappings; the approved DE artwork is byte-identical. Plain stripe fields retain every band; standalone symbols retain their proportions inside extended matching fields. Other flag sources use uniform centered cover. Language, flag and layout mappings are listed in language-flags.md.

The five material tiers are matte gray, satin silver, cobalt blue, gold and platinum. The immutable geometry snapshot retains its creation-stage review status; `sources/type/approval.json` records its subsequent approval for production without changing the approved source bytes.

## What complete means here

The user selected complete coverage of defined stream metadata and its associated language/provider lists. The pinned references are AIOStreams commit `f67d00ac6cd6d4efdde01f5d6f59bf1dbee95854`, `@viren070/parse-torrent-title` 0.8.8, the inspected Nuvio model/presentation contracts and StreamForge's `parse-torrent-title` 1.4.0 handlers. The collection also retains the extended common-media-format inventory prepared for this task.

Every one of **698 explicit source mappings** resolves to a delivered asset. The complete 240-entry language/region mapping, 18 service list and 25 parsed network list are represented. Aliases can refer to the same visible artwork while retaining separate source mappings. The generated assets contain 891 distinct text/material renders under 942 catalog paths; every path contains its own independent file.

Arbitrary titles, filenames, sizes, dates, bitrates, seed counts, release-group strings and new user-defined regular expressions are variable data, not a finite set of named format values. Their field-label assets are included; infinitely variable values are not claimed to be pre-rendered. This artwork library does not establish decoder support or implement stream classification. The app code is unchanged; the published matching configuration is in `manifest.json`.

## Brand graphics and compositions

Brand drawings are sourced from brand owners, official partner sites, upstream service configurations and documented public artwork mirrors/libraries. Their paths, colors and proportions are not redrawn by AI. Original source files, exact URLs and hashes are included. Standalone SVG namespace or physical-unit normalization only supplies a stable rendering container; original source bytes are retained.

Source resolution is recorded per mark. Smaller original raster files are faithfully resized for the 4K canvas; that does not invent new source detail. SVGs with embedded raster artwork are identified in the provenance. Preview backgrounds are presentation aids and are not added to the transparent canvas; any background intrinsic to an original mark is preserved.

The seven compositions join existing components without redrawing the brand mark. **DTS-HD and DTS-ES use the original DTS mark with the HD or ES format label.** They are explicitly labeled compositions, not representations of an original stand-alone variant lockup. Other compositions include Blu-ray REMUX, HDR with Dolby Vision, Dolby Vision ONLY and the DTS lossless/lossy descriptors.

Font software is a renamed Michroma derivative under SIL OFL 1.1; its license and attribution are in `sources/type`. Brand source attributions are in `data/brand-sources.json`. No blanket ownership or license claim is made for third-party trademarks.

## Files and review

- `manifest.json`: URL-importable Nuvio badge rules.
- `index.html`: offline searchable gallery, category/type filters, pagination and a 16-pixel preview mode.
- `masters/<category>/<id>.webp`: complete 4K masters.
- `web/<category>/<id>.webp`: cropped app copies, up to 768 x 512 pixels.
- `previews`: complete category contact sheets, a representative overview and type-consistency proofs.
- `data/catalog.json`: all assets, hashes, aliases, categories, source references and recommended preview backgrounds.
- `data/verification.json`: executed checks and source-coverage results.
- `data/source-coverage.json`: all expected source values mapped to delivered IDs.
- `sources`: unchanged brand originals, the approved type source and flat flag vector artwork.

The 16-pixel gallery mode follows the inspected Nuvio image height and maximum width for a layout preview. It is not an on-device runtime test. Long descriptors and wide original wordmarks scale smaller in that constrained slot; full-size masters remain available.

## Verification

- All 1037 catalog entries have a 4K master and an app copy.
- Every master was decoded and checked for 3840 x 2160 RGBA with a transparent-to-opaque alpha range.
- Every unique render passed an exact lossless encode/decode pixel comparison.
- Every delivered image checksum matches its production receipt; app copies also decode successfully.
- In this finalization, 20 changed asset pairs received fresh image-contract decoding. The other 1017 pairs retained their earlier decode checks after current SHA-256 comparisons established identical bytes.
- Every generated glyph occurrence references the approved glyph contour hash; unsupported characters fail explicitly.
- All 698 source mappings resolve, with zero missing assets and zero unresolved render errors.
- Category contact sheets and the gallery provide every asset for visual review.

## Category counts

| Category | Badges |
| --- | ---: |
| resolution | 35 |
| dynamic-range | 15 |
| video-codec | 35 |
| audio-codec | 35 |
| audio-channel | 32 |
| audio-detail | 21 |
| frame-rate | 22 |
| color | 20 |
| aspect-ratio | 22 |
| source | 58 |
| edition | 40 |
| projection | 20 |
| subtitles | 26 |
| language-mode | 22 |
| accessibility | 8 |
| container | 24 |
| delivery | 37 |
| availability | 60 |
| content | 15 |
| language | 227 |
| language-region | 57 |
| audio-brand | 12 |
| picture-brand | 8 |
| disc-brand | 5 |
| service | 50 |
| provider | 18 |
| general | 3 |
| edition-brand | 1 |
| proxy | 3 |
| release-group | 4 |
| release-site | 1 |
| stream-attribute | 16 |
| release-type | 5 |
| region | 23 |
| country | 4 |
| extension | 33 |
| metadata-field | 20 |
