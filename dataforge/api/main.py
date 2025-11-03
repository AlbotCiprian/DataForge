from fastapi import FastAPI
from routers.health import router as health_router
from routers.metadata import router as metadata_router

app = FastAPI(title="dataforge API", version="0.1.0")

app.include_router(health_router)
app.include_router(metadata_router)

