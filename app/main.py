from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.database import AsyncDatabase
from app.config import settings
from app.api.v1 import router

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """"""
    LOGGER.info("STARTING UP...")
    app.state.db = AsyncDatabase(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT
    )
    await app.state.db.connect()
    await app.state.db.drop_tables()
    await app.state.db.initdb()
    # await app.state.db.populate_with_dummy_data()

    yield

    LOGGER.info("SHUTTING DOWN...")
    await app.state.db.disconnect()
    LOGGER.info("DATABASE CLOSED SUCCESSFULLY")


app: FastAPI = FastAPI(
    title="JOB CONNECT API",
    description="On demand technical services plartform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root() -> dict:
    """"""
    return {
        "STATUS": f"{app.title} is running",
        "VERSION": app.version,
        "ENVIRONMENT": "production" if not settings.DEBUG else "development",
        "DOCS": "api/docs" if settings.DEBUG else None
    }


@app.get("/health")
async def health_check(db: AsyncDatabase = Depends(lambda: app.state.db)):
    """Database health check endpoint."""
    try:
        # Test database connection
        await db.fetchrow("SELECT 1")
        return {
            "STATUS": "healthy", 
            "DATABASE": "connected",
            "DEBUG": settings.DEBUG
        }
    except Exception as e:
        LOGGER.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "STATUS": "unhealthy", 
                "DATABASE": "disconnected",
                "ERROR": str(e)
            },
        )
