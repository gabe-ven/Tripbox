from pydantic import BaseModel, Field


class ScreenshotAnalysis(BaseModel):
    travel_related: bool
    place_name: str | None = None
    city: str | None = None
    country: str | None = None
    category: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
