import base64
import logging

import anthropic
from pydantic import ValidationError

from app.core.config import settings
from app.models.screenshot import CATEGORIES, ScreenshotAnalysis

logger = logging.getLogger(__name__)

# Image formats Claude accepts, keyed by the name detect_image_format() returns.
MEDIA_TYPES = {"jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}

SYSTEM_PROMPT = f"""You identify travel places in screenshots that people save \
for future trips: social media posts, maps, websites, and photos.

Decide whether the screenshot shows a specific real-world place someone could \
visit (restaurant, cafe, attraction, shop, hotel, beach, park, etc.). If it \
does not, set travel_related to false and every other field to null.

If several places appear, report only the main one the screenshot is about.

Use only evidence in the image: visible names, captions, location tags, \
addresses, signage, and recognizable landmarks. Give the place name as it \
appears or as it is commonly known. Fill in city and country only when the \
image shows them or the place is unambiguous; otherwise use null. Never invent \
a name.

category must be one of: {", ".join(CATEGORIES)}.

confidence is your probability (0 to 1) that place_name, city, and country are \
all correct. Lower it when the name is partial, the location is inferred, or \
the screenshot is ambiguous."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "travel_related": {"type": "boolean"},
        "place_name": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "city": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "country": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "category": {"anyOf": [{"type": "string", "enum": list(CATEGORIES)}, {"type": "null"}]},
        "confidence": {"anyOf": [{"type": "number"}, {"type": "null"}]},
    },
    "required": ["travel_related", "place_name", "city", "country", "category", "confidence"],
    "additionalProperties": False,
}


class ScreenshotAnalysisError(Exception):
    """Analysis failed; the message is safe to show to the user."""


_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            logger.error("ANTHROPIC_API_KEY is not set")
            raise ScreenshotAnalysisError("Screenshot analysis isn't configured on the server.")
        _client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key, timeout=60)
    return _client


def detect_image_format(data: bytes) -> str | None:
    # The client-supplied content type can't be trusted, so check the bytes.
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None


def parse_analysis(text: str) -> ScreenshotAnalysis:
    try:
        analysis = ScreenshotAnalysis.model_validate_json(text)
    except ValidationError:
        logger.warning("Model returned output that failed validation")
        raise ScreenshotAnalysisError("Couldn't understand this screenshot. Try again.")

    if not analysis.travel_related:
        return ScreenshotAnalysis(travel_related=False)
    return analysis


async def analyze_screenshot(image: bytes, image_format: str) -> ScreenshotAnalysis:
    client = _get_client()
    try:
        response = await client.messages.create(
            model=settings.claude_model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "medium",
                "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
            },
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": MEDIA_TYPES[image_format],
                            "data": base64.standard_b64encode(image).decode("ascii"),
                        },
                    },
                    {"type": "text", "text": "Identify the travel place in this screenshot."},
                ],
            }],
        )
    except anthropic.APIConnectionError:
        logger.exception("Could not reach the Claude API")
        raise ScreenshotAnalysisError("The analysis service is unreachable. Try again shortly.")
    except anthropic.RateLimitError:
        logger.warning("Claude API rate limit hit")
        raise ScreenshotAnalysisError("Too many screenshots at once. Wait a moment and try again.")
    except anthropic.APIStatusError as e:
        logger.error("Claude API error: status=%s type=%s", e.status_code, type(e).__name__)
        raise ScreenshotAnalysisError("Screenshot analysis failed. Try again.")

    if response.stop_reason != "end_turn":
        logger.warning("Unexpected stop_reason from Claude: %s", response.stop_reason)
        raise ScreenshotAnalysisError("Couldn't analyze this screenshot. Try a different one.")

    text = next((block.text for block in response.content if block.type == "text"), "")
    return parse_analysis(text)
