from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from information_retrieval.api.api_v1.routers import activities, brag_doc, users
from information_retrieval.app_lifespan_management import cleanup_app_state, init_app_state
from information_retrieval.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app_state(app)
    yield
    await cleanup_app_state(app)


app = FastAPI(title="Narrative Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.config.get("ALLOWED_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


app.include_router(users.router)
app.include_router(activities.router)
app.include_router(brag_doc.router)
