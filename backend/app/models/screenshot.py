from typing import Literal, get_args

from pydantic import BaseModel, Field, field_validator

Category = Literal["Food", "Cafe", "Attraction", "Shopping", "Hotel", "Nature", "Other"]
CATEGORIES = get_args(Category)


class ScreenshotAnalysis(BaseModel):
    travel_related: bool
    place_name: str | None = None
    city: str | None = None
    country: str | None = None
    category: Category | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)

    @field_validator("place_name", "city", "country", mode="before")
    @classmethod
    def blank_to_none(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value
