from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)

JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 100
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100


def upload(data: bytes, filename: str = "shot.jpg", content_type: str = "image/jpeg"):
    return client.post(
        "/analyze-screenshot", files={"file": (filename, data, content_type)}
    )


def test_returns_analysis_for_jpeg():
    response = upload(JPEG_BYTES)

    assert response.status_code == 200
    body = response.json()
    assert body["travel_related"] is True
    assert set(body) == {
        "travel_related", "place_name", "city", "country", "category", "confidence"
    }


def test_accepts_png():
    assert upload(PNG_BYTES, "shot.png", "image/png").status_code == 200


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
