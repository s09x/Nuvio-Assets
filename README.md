# Nuvio Assets

Custom artwork and hosted collection assets for Nuvio.

## Year collections

[`collections/by-year`](collections/by-year) contains nine distinct film covers. Labels run from 2026 through 2020, followed by 2015 (2015–2019) and 2010 (2010–2014).

## Discover collections

[`collections/discover/de`](collections/discover/de) contains six covers and their six hover variants.

## Decade collections

[`collections/by-decade`](collections/by-decade) contains six decade designs from the 2000s through the 1950s, each with its cover and hover variant.

## Genre collections

[`collections/genres/de`](collections/genres/de) contains 25 genre covers and their matching hover variants, with German headings and descriptions.

## Moods and atmosphere

[`collections/moods/de`](collections/moods/de) contains ten mood covers and their matching hover variants, with German headings and descriptions.

## Film collections

[`collections/film-collections/de`](collections/film-collections/de) contains 249 film-collection covers and the eleven available hover variants. Collection labels and other accompanying text are in German; film and franchise names retain their established titles.

## Additional collection assets

[`collections/hosted`](collections/hosted) contains 714 original image files: title logos, hero backdrops, and the remaining streaming-service, studio, and anime covers and hover images. Files are grouped by collection in `discover`, `streaming-services`, `genres`, `moods`, `studios`, `by-year`, `anime`, and `film-collections`.

These assets retain their original file contents, dimensions, and transparency in PNG, JPEG, WebP, or SVG format. The [manifest](collections/hosted/manifest.json) records each file's source, format, dimensions, checksum, and collection references.

## Using the images

The images are publicly accessible without authentication. Use the **raw image URL**, rather than a GitHub file-view page, in your Nuvio collection configuration.

For example, these fields configure the Action folder's images:

```json
{
  "coverImageUrl": "https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/collections/genres/de/action-cover-de-4k.webp",
  "focusGifUrl": "https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/collections/genres/de/action-hover-de-4k.webp",
  "focusGifEnabled": true,
  "hideTitle": true
}
```

The custom covers and hover variants are supplied as WebP files. Landscape cards are 3840 × 2160 pixels. Portrait posters retain their original aspect ratio with a 3840-pixel long edge. Their directories include a `manifest.json` with asset names, dimensions, and checksums. Original assets in `collections/hosted` retain their source resolution; SVG files are scalable.

URLs using `main` follow the current version; replace `main` with a commit SHA to reference a fixed version.

## Stream badges

[`badges`](badges) contains the approved 1,037-badge stream library: 4K masters, smaller app images, original brand graphics and 50 flat flag language badges. Release 2.0 uses original marks and neutral borderless typography, displays 4K for the 2160p alias, and preserves the approved centered DE/EN flags. The selected flag-language series excludes India mappings.

Use this URL in **Settings > Streams > Stream badge URLs** in Nuvio:

```text
https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/manifest.json
```

The import contains 1,037 rules in 37 groups. See the [badge documentation](badges/README.md), [language overview](badges/previews/language-flags.png) and [source catalog](badges/data/catalog.json) for the complete inventory, mapping behavior and attributions.
