# Nuvio Assets

Custom artwork for Nuvio.

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

Images are supplied as WebP files. Landscape cards are 3840 × 2160 pixels. Portrait posters retain their original aspect ratio with a 3840-pixel long edge. Each collection directory includes a `manifest.json` with asset names, dimensions, and checksums. URLs using `main` follow the current version; replace `main` with a commit SHA to reference a fixed version.
