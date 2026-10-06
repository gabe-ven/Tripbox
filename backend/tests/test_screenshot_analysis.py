import asyncio
import json

import pytest

from app.core.config import settings
from app.services import screenshot_analysis
from app.services.screenshot_analysis import ScreenshotAnalysisError, parse_analysis


def test_parses_valid_output():
    analysis = parse_analysis(json.dumps({
        "travel_related": True,
        "place_name": "Glitch Coffee",
        "city": "Tokyo",
        "country": "Japan",
        "category": "Cafe",
        "confidence": 0.8,
    }))

    assert analysis.place_name == "Glitch Coffee"
    assert analysis.category == "Cafe"


def test_non_travel_result_clears_other_fields():
    analysis = parse_analysis(json.dumps({
        "travel_related": False,
        "place_name": "Some Meme",
        "city": None,
        "country": None,
        "category": "Other",
        "confidence": 0.9,
    }))

    assert analysis.model_dump() == {
        "travel_related": False,
        "place_name": None,
        "city": None,
        "country": None,
        "category": None,
        "confidence": None,
    }


def test_blank_strings_become_null():
    analysis = parse_analysis(json.dumps({
        "travel_related": True,
        "place_name": "Dotonbori",
        "city": "  ",
        "country": "",
        "category": "Attraction",
        "confidence": 0.5,
    }))

    assert analysis.city is None
    assert analysis.country is None


@pytest.mark.parametrize("text", [
    "",
    "not json",
    '{"place_name": "Missing travel_related"}',
    '{"travel_related": true, "category": "Spaceport"}',
    '{"travel_related": true, "confidence": 1.7}',
])
def test_malformed_output_raises(text):
    with pytest.raises(ScreenshotAnalysisError):
        parse_analysis(text)


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.setattr(settings, "anthropic_api_key", "")
    monkeypatch.setattr(screenshot_analysis, "_client", None)

    with pytest.raises(ScreenshotAnalysisError, match="isn't configured"):
        asyncio.run(screenshot_analysis.analyze_screenshot(b"\xff\xd8\xff", "jpeg"))
