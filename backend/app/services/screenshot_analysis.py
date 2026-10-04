from app.models.screenshot import ScreenshotAnalysis

# Magic-number prefixes for the image formats we accept. The client-supplied
# content type can't be trusted, so the bytes themselves are checked.
_SIGNATURES = {
    "jpeg": (b"\xff\xd8\xff",),
    "png": (b"\x89PNG\r\n\x1a\n",),
}


def detect_image_format(data: bytes) -> str | None:
    for name, prefixes in _SIGNATURES.items():
        if data.startswith(prefixes):
            return name
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[4:8] == b"ftyp" and data[8:12] in (b"heic", b"heix", b"mif1", b"msf1"):
        return "heic"
    return None


def analyze_screenshot(image: bytes) -> ScreenshotAnalysis:
    """Temporary mock until the vision model is connected."""
    return ScreenshotAnalysis(
        travel_related=True,
        place_name="Shibuya Sky",
        city="Tokyo",
        country="Japan",
        category="Attraction",
        confidence=0.94,
    )
