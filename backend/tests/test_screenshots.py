import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.models.screenshot import ScreenshotAnalysis
from app.routes import screenshots
from app.services.screenshot_analysis import ScreenshotAnalysisError

client = TestClient(app)

JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 100
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
HEIC_BYTES = b"\x00\x00\x00\x18ftypheic" + b"\x00" * 100

SHIBUYA_SKY = ScreenshotAnalysis(
    travel_related=True,
    place_name="Shibuya Sky",
    city="Tokyo",
    country="Japan",
    category="Attraction",
    confidence=0.94,
)


@pytest.fixture(autouse=True)
def fake_analysis(monkeypatch):
    """Replace the Claude call so route tests never hit the network."""
    calls = []

    async def fake(image: bytes, image_format: str) -> ScreenshotAnalysis:
        calls.append(image_format)
        return SHIBUYA_SKY

    monkeypatch.setattr(screenshots, "analyze_screenshot", fake)
    return calls


def upload(data: bytes, filename: str = "shot.jpg", content_type: str = "image/jpeg"):
    return client.post(
        "/analyze-screenshot", files={"file": (filename, data, content_type)}
    )


def test_returns_analysis_for_jpeg(fake_analysis):
    response = upload(JPEG_BYTES)

    assert response.status_code == 200
    assert response.json() == SHIBUYA_SKY.model_dump()
    assert fake_analysis == ["jpeg"]


def test_accepts_png(fake_analysis):
    assert upload(PNG_BYTES, "shot.png", "image/png").status_code == 200
    assert fake_analysis == ["png"]


def test_rejects_heic_which_claude_cannot_read():
    assert upload(HEIC_BYTES, "shot.heic", "image/heic").status_code == 415


def test_rejects_non_image_even_with_image_content_type():
    response = upload(b"not an image at all", "shot.jpg", "image/jpeg")

    assert response.status_code == 415


def test_rejects_empty_file():
    assert upload(b"").status_code == 400


def test_rejects_oversized_file(monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", 50)

    response = upload(JPEG_BYTES)

    assert response.status_code == 413


def test_requires_file():
    assert client.post("/analyze-screenshot").status_code == 422


def test_analysis_failure_returns_502_with_message(monkeypatch):
    async def failing(image: bytes, image_format: str) -> ScreenshotAnalysis:
        raise ScreenshotAnalysisError("Screenshot analysis failed. Try again.")

    monkeypatch.setattr(screenshots, "analyze_screenshot", failing)

    response = upload(JPEG_BYTES)

    assert response.status_code == 502
    assert response.json() == {"detail": "Screenshot analysis failed. Try again."}
