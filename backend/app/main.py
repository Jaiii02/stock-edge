from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_ORIGINS
from app.api.routes_analysis import router as analysis_router
from app.api.routes_health import router as health_router
from app.api.routes_stocks import router as stocks_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(stocks_router)
app.include_router(analysis_router)

# Versioned contract for new clients. The original routes remain available
# temporarily so the current frontend continues to work during migration.
app.include_router(health_router, prefix="/api/v1")
app.include_router(stocks_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
