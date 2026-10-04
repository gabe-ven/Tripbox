import logging

from fastapi import FastAPI

from app.core.config import settings
from app.routes import health

logging.basicConfig(level=settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(health.router)
