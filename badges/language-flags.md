# Nuvio: 50 language flag badges

User-approved 50-language flag series. It is included in the main Nuvio import: https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/manifest.json

This is the user-selected collection of **50 common film and series languages**, with **India mappings excluded**. It is a curated stream-language selection, not a measured popularity ranking or worldwide speaker-count ranking. It uses 38 languages from the existing AIOStreams parser language list, supplemented with 12 additional languages already present in the complete Nuvio badge catalog. Regional variants do not inflate the language count.

Each badge has a **3840 x 2160 lossless WebP RGBA master** and a separate cropped app copy. The approved lettering, spacing, materials and frame remain intact. The flat flag covers the complete interior; the exterior remains transparent. There are no waving, fabric or flag-shadow effects. All **DE files are byte-identical to the user's approved example**.

## Artwork and flag mapping

The unchanged DE flag construction retains the approved three equal horizontal bands and colors. Other flags use the original flat SVG sources from `lipis/flag-icons`, pinned to `086f7e97d657358203916dbe84f61c2bccaa81eb`. Original bytes and the MIT license are included in `sources/flags`. Plain stripe fields adapt to the full interior while preserving every band and its relative width or height. Standalone symbols on solid-color flags are uniformly scaled to fit completely within matching extended fields. Greece retains all nine bands and a square canton with equal-width cross arms; its source-derived field layout is included in `sources/flags/adaptive`. Other flags use uniform centered cover, with edge cropping according to badge proportions. Opaque underlays close transparent antialiasing seams in source paths. Flag symbols are never stretched or shaded; no flag is redrawn by an image model. The exact layout policy is recorded per badge.

The existing AIOStreams priority mapping selects the Union Jack for EN and the mainland-China flag for ZH. Catalan, Basque and Galician use their regional flags; Cantonese uses Hong Kong as its display convention. These are visible language-selection conventions, with their basis recorded per entry. The eight parser entries mapped to India were replaced within this 50-language selection: Hindi, Punjabi, Marathi, Gujarati, Tamil, Telugu, Kannada and Malayalam. Existing assets elsewhere in the full catalog were preserved.

The fixed type source and OFL license are included in `sources/type`. Its geometry SHA-256 remains `2104dd08a14327ad320e4e32524ddf94f588ab39876fddf2caf1e536ddd69d06`.

## Review files

- `language-flags.html`: searchable offline gallery with dark/light backgrounds and a 32-pixel preview mode.
- `previews/language-flags-01.png` and `previews/language-flags-02.png`: all 50 badges on two contact sheets.
- `previews/language-flags.png`: all 50 badges on one sheet.
- `masters/language`: 4K masters.
- `web/language`: cropped app copies.
- `data/language-flag-selection.json`: exact selection, exclusion and flag-mapping evidence.
- `data/language-flag-series-verification.json`: delivered hashes and per-asset foreground/background checks.
- `data/language-flag-layout-checks.json`: complete stripe-pattern and circular-symbol checks.

The stand-alone ZIP also provides this gallery as `index.html` and this guide as `README.md`. Gallery file links and JavaScript syntax are checked statically. Interactive browser testing was unavailable because local-file navigation was blocked by the browser policy.

## Executed artwork checks

All 50 master/app pairs are present with the expected checksums. Revised images passed lossless encode/decode comparisons. Every flag interior is fully opaque, approved glyph contours are reused without change, opaque foreground pixels are identical, and pixels outside the added background support remain identical. The approved DE files retain their exact earlier checksums. No flag maps to IN. The alias `country/uk` remains unchanged while the separate language asset `language/uk` receives Ukraine's flag.

## Language and flag list

| Badge | Language | Flag |
| --- | --- | --- |
| DE | German | Germany (DE) |
| EN | English | United Kingdom (GB) |
| FR | French | France (FR) |
| ES | Spanish | Spain (ES) |
| IT | Italian | Italy (IT) |
| PT | Portuguese | Portugal (PT) |
| JA | Japanese | Japan (JP) |
| ZH | Chinese | China (CN) |
| KO | Korean | South Korea (KR) |
| RU | Russian | Russia (RU) |
| AR | Arabic | Saudi Arabia (SA) |
| BN | Bengali | Bangladesh (BD) |
| TH | Thai | Thailand (TH) |
| VI | Vietnamese | Vietnam (VN) |
| ID | Indonesian | Indonesia (ID) |
| TR | Turkish | Türkiye (TR) |
| HE | Hebrew | Israel (IL) |
| FA | Persian | Iran (IR) |
| UK | Ukrainian | Ukraine (UA) |
| EL | Greek | Greece (GR) |
| LT | Lithuanian | Lithuania (LT) |
| LV | Latvian | Latvia (LV) |
| ET | Estonian | Estonia (EE) |
| PL | Polish | Poland (PL) |
| CS | Czech | Czech Republic (CZ) |
| SK | Slovak | Slovakia (SK) |
| HU | Hungarian | Hungary (HU) |
| RO | Romanian | Romania (RO) |
| BG | Bulgarian | Bulgaria (BG) |
| SR | Serbian | Serbia (RS) |
| HR | Croatian | Croatia (HR) |
| SL | Slovenian | Slovenia (SI) |
| NL | Dutch | Netherlands (NL) |
| DA | Danish | Denmark (DK) |
| FI | Finnish | Finland (FI) |
| SV | Swedish | Sweden (SE) |
| NO | Norwegian | Norway (NO) |
| MS | Malay | Malaysia (MY) |
| UR | Urdu | Pakistan (PK) |
| TL | Tagalog | Philippines (PH) |
| IS | Icelandic | Iceland (IS) |
| BS | Bosnian | Bosnia and Herzegovina (BA) |
| SQ | Albanian | Albania (AL) |
| MK | Macedonian | North Macedonia (MK) |
| CA | Catalan | Catalonia (ES-CT) |
| EU | Basque | Basque Country (ES-PV) |
| GL | Galician | Galicia (ES-GA) |
| KA | Georgian | Georgia (GE) |
| HY | Armenian | Armenia (AM) |
| YUE | Cantonese | Hong Kong (HK) |
