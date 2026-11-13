"""Build a curated, deduplicated Nuvio/Fusion-compatible badge import from catalog.json."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
BASE_URL = "https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/"
LEFT = r"(?<![\p{L}\p{N}])"
RIGHT = r"(?![\p{L}\p{N}+])"
SEP = r"[ ._-]*"

CONTEXTS = {
    "resolution": "resolution|quality|video",
    "picture-brand": "hdr|range|video|picture",
    "dynamic-range": "hdr|range|video",
    "color": "color|bit|video",
    "video-codec": "video|codec|format",
    "audio-brand": "audio|codec|format",
    "audio-codec": "audio|codec|format",
    "audio-channel": "channels?|audio|layout",
    "disc-brand": "source|quality|format|disc",
    "source": "source|quality|format",
    "edition": "edition|cut|version",
    "language": "lang(?:uage)?s?|audio|sprache|sprachen",
    "language-mode": "lang(?:uage)?s?|audio|mode",
    "subtitles": "subtitles?|subs?",
    "container": "container|extension|format",
}

COMMON_SHORT = {
    "AVC", "AV1", "VP9", "AAC", "MP3", "PCM", "DTS", "HLG", "SDR",
    "OV", "OMU", "SUBS", "SDH", "HDR", "4K", "2K", "UHD", "FHD", "DVD",
}

LANGUAGE_ALIASES = {
    "de": ["German", "Deutsch", "GER", "DEU"], "en": ["English", "ENG"],
    "fr": ["French", "Français", "FRE", "FRA"], "es": ["Spanish", "Español", "SPA"],
    "it": ["Italian", "Italiano", "ITA"], "pt": ["Portuguese", "Português", "POR"],
    "ja": ["Japanese", "日本語", "JPN"], "zh": ["Chinese", "中文", "Mandarin", "CHI", "ZHO"],
    "ko": ["Korean", "한국어", "KOR"], "ru": ["Russian", "Русский", "RUS"],
    "ar": ["Arabic", "العربية", "ARA"], "bn": ["Bengali", "Bangla", "বাংলা", "BEN"],
    "th": ["Thai", "ไทย", "THA"], "vi": ["Vietnamese", "Tiếng Việt", "VIE"],
    "id": ["Indonesian", "Bahasa Indonesia", "IND"], "tr": ["Turkish", "Türkçe", "TUR"],
    "he": ["Hebrew", "עברית", "HEB"], "fa": ["Persian", "Farsi", "فارسی", "PER", "FAS"],
    "uk": ["Ukrainian", "Українська", "UKR"], "el": ["Greek", "Ελληνικά", "GRE", "ELL"],
    "lt": ["Lithuanian", "Lietuvių", "LIT"], "lv": ["Latvian", "Latviešu", "LAV"],
    "et": ["Estonian", "Eesti", "EST"], "pl": ["Polish", "Polski", "POL"],
    "cs": ["Czech", "Čeština", "CZE", "CES"], "sk": ["Slovak", "Slovenčina", "SLO", "SLK"],
    "hu": ["Hungarian", "Magyar", "HUN"], "ro": ["Romanian", "Română", "RUM", "RON"],
    "bg": ["Bulgarian", "Български", "BUL"], "sr": ["Serbian", "Српски", "SRP"],
    "hr": ["Croatian", "Hrvatski", "HRV"], "sl": ["Slovenian", "Slovenščina", "SLV"],
    "nl": ["Dutch", "Nederlands", "DUT", "NLD"], "da": ["Danish", "Dansk", "DAN"],
    "fi": ["Finnish", "Suomi", "FIN"], "sv": ["Swedish", "Svenska", "SWE"],
    "no": ["Norwegian", "Norsk", "NOR"], "ms": ["Malay", "Bahasa Melayu", "MAY", "MSA"],
    "ur": ["Urdu", "اردو", "URD"], "tl": ["Tagalog", "Filipino", "TGL", "FIL"],
    "is": ["Icelandic", "Íslenska", "ICE", "ISL"], "bs": ["Bosnian", "Bosanski", "BOS"],
    "sq": ["Albanian", "Shqip", "ALB", "SQI"], "mk": ["Macedonian", "Македонски", "MAC", "MKD"],
    "ca": ["Catalan", "Català", "CAT"], "eu": ["Basque", "Euskara", "BAQ", "EUS"],
    "gl": ["Galician", "Galego", "GLG"], "ka": ["Georgian", "ქართული", "GEO", "KAT"],
    "hy": ["Armenian", "Հայերեն", "ARM", "HYE"], "yue": ["Cantonese", "粵語", "粤语", "YUE"],
}

EXTRA_ALIASES = {
    "resolution/4k": ["2160p", "4K UHD", "UHD", "DCI 4K"],
    "resolution/1440p": ["2K", "QHD", "WQHD"],
    "resolution/1080p": ["FHD", "Full HD"],
    "dynamic-range/upscaled": ["AI Upscale", "AI Upscaled"],
    "video-codec/avc": ["H.264", "H264", "x264"],
    "video-codec/hevc": ["H.265", "H265", "x265"],
    "audio-brand/dolby-digital": ["AC-3", "AC3"],
    "audio-brand/dolby-digital-plus": ["Dolby Digital+", "E-AC-3", "EAC3", "E-AC3"],
    "audio-codec/pcm": ["LPCM"],
    "audio-channel/2-0": ["Stereo"],
    "audio-channel/1-0": ["Mono"],
    "disc-brand/blu-ray": ["Blu-ray", "UHD BluRay", "UHD Blu-ray"],
    "source/remux": ["BluRay REMUX", "UHD REMUX", "BDREMUX"],
    "source/web-dl": ["WEBDL", "UHD WEB-DL"],
    "source/webrip": ["WEB-Rip"],
    "source/bdrip": ["BRRip", "UHD BDRip"],
    "source/hdrip": ["UHDRip"],
    "edition/director-cut": ["Directors Cut"],
    "language-mode/multi": ["Multi Audio", "Multilingual"],
    "subtitles/multi-subs": ["Multi-Subs", "Multiple Subtitle", "Multiple Subtitles", "MultiSub", "MultiSubs"],
    "subtitles/hardsub": ["Hardsubs", "Hardcoded"],
}

LINE_START = r"(?:^|[\r\n])"

SPECIAL = {
    "audio-codec/aac": LEFT + r"(?:x?HE[ ._-]*)?AAC(?![\p{L}])",
    "dynamic-range/hdr": (
        LINE_START + r"(?![^\r\n]*?" + LEFT + r"(?:HDR[ ._-]*10|HLG)(?![\p{L}\p{N}]))"
        + r"[^\r\n]*?" + LEFT + r"HDR" + RIGHT + r"(?![ ._-]*(?:10|HLG|ONLY|PQ|TO|\+|DOLBY))"
    ),
    "dynamic-range/hdr10": LEFT + r"HDR[ ._-]*10(?![\p{L}\p{N}+]|[ ._-]*(?:PLUS|ADVANCED|GAMING))",
    "picture-brand/hdr10plus": LEFT + r"HDR[ ._-]*10(?:\+|[ ._-]*PLUS)" + RIGHT,
    "picture-brand/imax": (
        LINE_START + r"(?![^\r\n]*?" + LEFT + r"IMAX[ ._-]*(?:ENHANCED|RATIO)(?![\p{L}\p{N}]))"
        + r"[^\r\n]*?" + LEFT + r"IMAX" + RIGHT + r"(?![ ._-]*(?:ENHANCED|RATIO))"
    ),
    "picture-brand/dolby-vision": LEFT + r"(?:DOLBY[ ._-]*VISION|DOVI|DV)" + RIGHT,
    "audio-brand/dolby-digital": LEFT + r"(?:(?<!E[ ._-])AC[ ._-]*3|DOLBY[ ._-]*DIGITAL|DD)(?![\p{L}+]|[ ._-]*PLUS)",
    "audio-brand/dolby-digital-plus": LEFT + r"(?:DOLBY[ ._-]*DIGITAL(?:[ ._-]*PLUS|\+)|E[ ._-]*AC[ ._-]*3|EAC3|E-AC3|DDP|DD\+)(?![\p{L}])",
    "audio-brand/dts": (
        LINE_START + r"(?![^\r\n]*?" + LEFT + r"DTS[ ._:-]*(?:HD|ES|X)(?![\p{L}\p{N}]))"
        + r"[^\r\n]*?" + LEFT + r"DTS" + RIGHT + r"(?![ ._:-]*(?:HD|ES|X|LOSSLESS|LOSSY))"
    ),
    "audio-brand/dts-hd": (
        LINE_START + r"(?![^\r\n]*?" + LEFT + r"DTS[ ._-]*HD[ ._-]*(?:MA|MASTER)(?![\p{L}\p{N}]))"
        + r"[^\r\n]*?" + LEFT + r"DTS[ ._-]*HD" + RIGHT + r"(?![ ._-]*(?:MA|MASTER))"
    ),
    "audio-brand/dts-hd-ma": LEFT + r"DTS[ ._-]*HD[ ._-]*(?:MA|MASTER[ ._-]*AUDIO)" + RIGHT,
    "audio-brand/dts-x": LEFT + r"DTS[ ._:-]*X" + RIGHT,
    "language-mode/multi": LEFT + r"MULTI(?:[ ._-]*(?:AUDIO|LINGUAL))?" + RIGHT + r"(?![ ._-]*SUBS?)",
    "subtitles/subs": (
        LINE_START + r"(?![^\r\n]*?" + LEFT + r"(?:MULTI|DUAL|NO|FULL|OCR)[ ._-]*SUBS?(?![\p{L}\p{N}]))"
        + r"[^\r\n]*?" + LEFT + r"SUBS" + RIGHT
    ),
}


def token(value):
    value = str(value).strip()
    escaped = re.escape(value)
    escaped = escaped.replace(r"\ ", r"[ ._-]+").replace(r"\-", SEP)
    return escaped


def bounded(values):
    values = sorted({value for value in values if value}, key=lambda value: (-len(value), value))
    return LEFT + "(?:" + "|".join(token(value) for value in values) + ")" + RIGHT if values else ""


def explicit(identifier):
    if identifier == "resolution/4k":
        return r"\[\s*badge\s*:\s*resolution/(?:4k|2160p)\s*\]"
    return r"\[\s*badge\s*:\s*" + re.escape(identifier) + r"\s*\]"


def context(category, values):
    names = CONTEXTS.get(category, re.escape(category).replace(r"\-", SEP))
    return LEFT + "(?:" + names + r")[ \t]*[:=][ \t]*(?:" + "|".join(token(value) for value in sorted(set(values), key=lambda value: -len(value))) + ")" + RIGHT


def compile_pattern(item, flags):
    identifier = item["id"]
    category = item["category"]
    label = item["label"]
    raw = [label, item["name"], *item.get("aliases", []), *EXTRA_ALIASES.get(identifier, [])]
    values = list(dict.fromkeys(value for value in (re.sub(r"^\d+:", "", str(value)).strip() for value in raw if value) if value))
    parts = [explicit(identifier)]
    mode = "metadata label and contextual aliases"
    if category == "language":
        code = identifier.split("/")[-1]
        language_values = LANGUAGE_ALIASES.get(code)
        parts.append(context(category, [label, *values]))
        if language_values:
            language_terms = "(?:" + "|".join(token(value) for value in sorted(language_values, key=lambda value: -len(value))) + ")"
            parts.append(context(category, language_values))
            parts.append(r"(?:^|[|/,;\[({\r\n])[ \t]*" + language_terms + r"[ \t]*(?=$|[|/,;\])}\r\n])")
            release_context = LEFT + r"(?:(?:19|20)\d{2}|S\d{1,3}E\d{1,3}|\d{3,4}[pi]|WEB[ ._-]*DL|BLU[ ._-]*RAY|REMUX)" + RIGHT
            parts.append(release_context + r"[^\r\n]{0,240}?" + bounded(language_values))
            parts.append(r"[\[({][ \t]*" + re.escape(label) + r"[ \t]*[\])}]")
            country = flags.get(identifier)
            if country and len(country) == 2:
                parts.append("".join(chr(127397 + ord(character)) for character in country))
            mode = "selected language names, ISO-639-2 aliases, explicit language codes and flag markers"
        else:
            mode = "explicit language metadata"
    elif identifier in SPECIAL:
        parts.append(SPECIAL[identifier])
    elif category == "audio-channel" and re.fullmatch(r"\d+(?:\.\d+)+", label):
        number = re.escape(label)
        suffix = r"(?![\p{L}\p{N}]|[._]\d)"
        extra_words = [value for value in values if value != label]
        parts.extend([
            r"^[ \t]*" + number + r"[ \t]*$",
            context(category, values),
            LEFT + r"(?:(?:x?HE[ ._-]*)?AAC|E?[ ._-]*AC[ ._-]?3|DDP|DD\+|DD|DTS(?:[ ._:-]*(?:X|ES|HD(?:[ ._-]*(?:MA|HRA|HR))?))?|TRUEHD|ATMOS|FLAC|OPUS|L?PCM|MP3)(?:[ ._-]*ATMOS)?[ ._-]*" + number + suffix,
            LEFT + number + r"[ ._-]*(?:CH(?:ANNELS?)?|SURROUND)" + RIGHT,
        ])
        if extra_words:
            parts.append(bounded(extra_words))
        mode = "channel metadata or audio codec context"
    elif category == "container":
        parts.append(r"\." + "(?:" + "|".join(re.escape(value.lstrip(".")) for value in values) + r")(?:$|[\s\]})?#])")
        parts.append(context("container", values))
        mode = "file extension or container metadata"
    else:
        automatic = [value for value in values if len(value) > 3 or value.upper() in COMMON_SHORT]
        if automatic:
            parts.append(bounded(automatic))
        parts.append(context(category, values))
        if category in {"resolution", "source", "audio-codec"}:
            short_values = [value for value in values if value not in automatic]
            if short_values:
                parts.append(r"^[ \t]*(?:" + "|".join(token(value) for value in short_values) + r")[ \t]*$")
    return "(?i)(?:" + "|".join(dict.fromkeys(part for part in parts if part)) + ")", mode


def main():
    catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
    selection = json.loads((ROOT / "data/language-flag-selection.json").read_text(encoding="utf-8"))
    selected_flags = {entry["asset_id"]: entry["country_code"] for entry in selection["entries"]}
    assert len(selected_flags) == 50 and "IN" not in selected_flags.values()
    filters = []
    modes = []
    four_k = next(item for item in catalog["items"] if item["id"] == "resolution/4k")
    canonical_images = {four_k["web_sha256"]: four_k["web"]}
    for item in catalog["items"]:
        image = ROOT / item["web"]
        assert hashlib.sha256(image.read_bytes()).hexdigest() == item["web_sha256"], item["id"]
        # Nuvio deduplicates by image URL. Byte-identical aliases share a URL.
        image_path = canonical_images.setdefault(item["web_sha256"], item["web"])
        pattern, mode = compile_pattern(item, selected_flags)
        image_url = BASE_URL + image_path + "?v=" + item["web_sha256"][:16]
        filters.append({"id": item["id"], "groupId": item["category"], "name": item["name"], "pattern": pattern, "imageURL": image_url, "isEnabled": True, "type": "filter"})
        modes.append({"id": item["id"], "matching": mode, "image_path": image_path})
    categories = list(dict.fromkeys(item["category"] for item in catalog["items"]))
    groups = [{"id": category, "name": category.replace("-", " ").title(), "color": "#9EB3D1", "isExpanded": True} for category in categories]
    payload = {
        "name": "Nuvio Stream Badges",
        "version": "2.1.0",
        "description": f"{len(filters)} curated borderless badges across {len(groups)} categories: original marks, neutral metadata labels, an approved HDR10 derivative and 50 centered flat flag languages.",
        "homepage": "https://github.com/s09x/Nuvio-Assets/tree/main/badges",
        "filters": filters,
        "groups": groups,
    }
    assert len(filters) == len({row["id"] for row in filters}) == len(catalog["items"])
    (ROOT / "manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "data/import-matching.json").write_text(json.dumps({"schema": "Nuvio/Fusion filters and groups", "matching_notes": "Nuvio searches available stream text. Missing metadata cannot be inferred. Every asset also supports [badge:category/id].", "filters": modes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"filters": len(filters), "groups": len(groups), "distinct_app_images": len(canonical_images), "flag_languages": len(selected_flags), "manifest_bytes": (ROOT / "manifest.json").stat().st_size, "import_url": BASE_URL + "manifest.json"}), flush=True)


if __name__ == "__main__":
    main()
