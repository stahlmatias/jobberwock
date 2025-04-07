from fastapi import FastAPI
from app.api.routes import router
from app.logger_config import setup_logger

setup_logger()

app = FastAPI(title="Jobberwocky")
app.include_router(router)