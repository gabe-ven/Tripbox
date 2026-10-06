import logging

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.core.config import settings
from app.models.screenshot import ScreenshotAnalysis
from app.services.screenshot_analysis import (
    ScreenshotAnalysisError,
    analyze_screenshot,
    detect_image_format,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze-screenshot", response_model=ScreenshotAnalysis)
async def analyze_screenshot_route(file: UploadFile) -> ScreenshotAnalysis:
    data = await file.read(settings.max_upload_bytes + 1)

    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The uploaded file is empty.")
    if len(data) > settings.max_upload_bytes:
        limit_mb = settings.max_upload_bytes // (1024 * 1024)
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE,
            f"Screenshot is too large. The limit is {limit_mb} MB.",
        )

    image_format = detect_image_format(data)
    if image_format is None:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Unsupported file type. Upload a JPEG, PNG, or WebP image.",
        )

    logger.info("Analyzing screenshot: format=%s size=%d bytes", image_format, len(data))
    try:
        return await analyze_screenshot(data, image_format)
    except ScreenshotAnalysisError as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(e))
