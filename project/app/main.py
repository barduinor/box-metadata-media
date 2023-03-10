"""fast api service to automatically apply metadata to media files stored in box"""
# project/app/main.py

from fastapi import FastAPI

from app.api import file, folder, info, metadata


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    application = FastAPI()
    application.include_router(info.router)
    application.include_router(metadata.router)
    application.include_router(file.router)
    application.include_router(folder.router)
    return application


app = create_application()
