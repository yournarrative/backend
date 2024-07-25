from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from information_retrieval.api.v1.routers import activities, users
from information_retrieval.core.config import settings
from information_retrieval.core.lifespan import cleanup_app_state, init_app_state


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
