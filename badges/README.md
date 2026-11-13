# Nuvio stream badges

Release **2.1.0** contains **136 curated badges in 15 categories**: 18 original-logo assets, 67 neutral text labels, 50 static language flags and one user-approved HDR10 derivative (with crisp white text/ink adapted for dark mode). Every entry has a **1280 x 720 lossless WebP RGBA master** and a smaller app image.

## Import into Nuvio

Open **Settings > Streams > Stream badge URLs**, add or refresh this URL and activate the import:

```text
https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/manifest.json
```

`4k` matches `2160p`, `4K`, `4K UHD`, `UHD`, `DCI 4K`, and `[badge:resolution/2160p]`. Matching runs in category priority order:

1. `resolution` (360p – 4K)
2. `picture-brand` (Dolby Vision, HDR10+, IMAX, IMAX Enhanced)
3. `dynamic-range` (HDR10, HDR, HLG, SDR, Upscaled)
4. `color` (10-bit)
5. `video-codec` (AV1, HEVC/x265/H.265, AVC/x264/H.264, VP9, VC-1, MPEG-2, XviD, DivX)
6. `audio-brand` (Dolby Atmos, Dolby TrueHD, Dolby Digital Plus/E-AC-3, Dolby Digital/AC-3, DTS:X, DTS-HD MA, DTS-HD, DTS-ES, DTS)
7. `audio-codec` (FLAC, Opus, AAC, PCM/LPCM, MP3)
8. `audio-channel` (7.1, 6.1, 5.1, 2.0/Stereo, 1.0/Mono)
9. `disc-brand` (Blu-ray Disc, DVD)
10. `source` (REMUX, WEB-DL, WEBRip, HDTV, BDRip, HDRip, DVDRip, IPTV)
11. `edition` (Theatrical, Extended, Director Cut, Final Cut, Uncut, Unrated, Uncensored, Remastered, Restored, IMAX Ratio, Open Matte, Hybrid, Proper, Repack, Complete)
12. `language` (50 flat flag badges)
13. `language-mode` (Multi, Dual Audio, Original, OV, OMU, Dubbed, Subbed)
14. `subtitles` (Multi Subs, Subs, Forced, SDH, Hardsub)
15. `container` (MKV, MP4, M4V, WEBM, M2TS)

Streaming services, debrid/usenet providers, proxy/delivery tags, metadata field labels, obsolete formats and unflagged minor language codes are intentionally excluded to avoid false positives, duplicate badges and regex overhead on Nuvio stream cards and player overlays.

## Approved design

Original graphics preserve their original identity, colors and proportions. Technical values without a verified exact mark use JetBrains Sans SemiBold in neutral off-white. There are **no added badge frames, outlines, shadows, metallic effects or category color accents**.

HDR10 is the explicitly approved derivative of the supplied HDR10+ image (plus removed, zero closed). The 50 selected language flags retain the established country/region mappings and exclude India assignments; see [language mappings](language-flags.md).

## Rebuild and verify

```sh
python badges/tools/build_manifest.py
pwsh -File badges/tools/verify_manifest.ps1
```

- `manifest.json`: curated Nuvio import (136 filters in 15 groups).
- `masters/` and `web/`: 272 approved WebP artwork files.
- `index.html`: offline searchable gallery.
- `previews/`: contact sheets for all 15 categories and overview.
- `data/catalog.json`: artwork paths, checksums and provenance.
- `data/import-verification.json`, `data/verification.json`, `data/gallery-checks.json`: executed verification reports.
