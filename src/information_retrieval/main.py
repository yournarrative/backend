from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from information_retrieval.api.api_v1.model.activity import UserActivities
# from information_retrieval.api.api_v1.model.query import Query, RAGResponse
from information_retrieval.api.api_v1.model.users import NarrativeUser
from information_retrieval.app_lifespan_management import init_app_state, cleanup_app_state
from information_retrieval.connectors.supabase.crud import \
    get_user_email_by_id, insert_new_user_activities
from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app_state(app.state)
    yield
    await cleanup_app_state(app.state)


app = FastAPI(title="Narrative", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yournarrative.io", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


@app.get('/users/{user_id}')
async def get_user_data(user_id: str, request: Request) -> Dict:
    logger.debug("New request to /users/{user_id} endpoint")
    try:
        user: NarrativeUser = await get_user_email_by_id(request.app.state.supabase_client, user_id)
        return dict(user)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@app.post("/api-v1/insert/insertActivities/")
async def insert_document(data: UserActivities, request: Request):
    logger.debug("New request to /api-v1/insert/insertActivities/ endpoint")
    try:
        await insert_new_user_activities(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
            activities=data.activities
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


# @app.post("/api-v1/activities/getActivitiesForUser/")

if __name__ == "__main__":
    uvicorn.run(app)
