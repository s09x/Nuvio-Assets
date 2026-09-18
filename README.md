# Nuvio Assets

Custom artwork for Nuvio collections. All 33 current cover and hover assets are 3840 × 2160 WebP images.

## Year collections

`collections/by-year` contains nine distinct film covers. Labels run from 2026 through 2020, followed by 2015 (2015–2019) and 2010 (2010–2014). Previously published filenames remain unchanged.

## Discover collections in German

`collections/discover/de` contains six covers and their six hover variants. Both headline and subtitle are translated into German. Source motifs, background, colors, and hover borders are retained. Original pixels outside the text regions were restored before upscaling.

## Existing decade collections

`collections/by-decade` contains the original six decade designs from the 2000s through the 1950s, each with its cover and hover variant. They were upscaled from 2560 × 1440 to 3840 × 2160 without regenerating the artwork or changing the text, motifs, colors, or layout.

## Production

The approved images were edited with `gpt-image-2.5-sunburst` through the Image API and resized from the best available PNG masters using Lanczos. They are 4K outputs, not native 4K generations. Lossless PNG masters are retained in the delivery package; WebP assets use quality 95 for Nuvio. Directory manifests record the dimensions and checksums.
