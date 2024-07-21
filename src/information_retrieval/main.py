from collections import defaultdict
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from information_retrieval.api.api_v1.model.activity import InsertActivitiesForUserRequest, Activity, ActivityWithID
from information_retrieval.api.api_v1.model.brag_doc import BragDoc, BragDocUpdateRequest
from information_retrieval.api.api_v1.model.checkin import CheckIn
from information_retrieval.api.api_v1.model.users import NarrativeUser
from information_retrieval.api.api_v1.processing.checkin import create_activities_from_check_in
from information_retrieval.app_lifespan_management import init_app_state, cleanup_app_state
from information_retrieval.connectors.supabase.crud import \
    get_user_email_by_id, insert_new_user_activities, get_activities_by_user_id, \
    create_brag_doc, get_brag_doc_data, update_brag_doc, update_activity_by_id
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
    allow_origins=["https://yournarrative.io", "http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


get_users_endpoint = "/api-v1/users/getUserInformation/{user_id}"
@app.get(get_users_endpoint)
async def get_user_data(user_id: str, request: Request) -> NarrativeUser:
    logger.debug(f"New request to {get_users_endpoint} endpoint")
    try:
        user: NarrativeUser = await get_user_email_by_id(request.app.state.supabase_client, user_id)
        return user

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


insert_activities_endpoint = "/api-v1/activities/insertActivities/"
@app.post(insert_activities_endpoint)
async def insert_activities(data: InsertActivitiesForUserRequest, request: Request):
    logger.debug(f"New request to {insert_activities_endpoint} endpoint")
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


get_activities_endpoint = "/api-v1/activities/getActivitiesForUser/{user_id}"
@app.get(get_activities_endpoint)
async def get_activities_for_user(user_id: str, request: Request) -> List[ActivityWithID]:
    logger.debug(f"New request to {get_activities_endpoint} endpoint")
    try:
        activities: List[ActivityWithID] = await get_activities_by_user_id(
            supabase=request.app.state.supabase_client,
            user_id=user_id,
        )
        return activities
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


update_activity_endpoint = "/api-v1/activities/updateActivity/"
@app.post(update_activity_endpoint)
async def update_activity(data: ActivityWithID, request: Request):
    logger.debug(f"New request to {update_activity_endpoint} endpoint")
    try:
        await update_activity_by_id(
            supabase=request.app.state.supabase_client,
            activity_with_id=data,
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


get_brag_doc_endpoint = "/api-v1/brag-doc/getBragDocForUser/{user_id}"
@app.get(get_brag_doc_endpoint)
async def get_brag_doc_for_user(user_id: str, request: Request) -> BragDoc:
    logger.debug(f"New request to {get_brag_doc_endpoint} endpoint")
    try:
        brag_doc: BragDoc = await get_brag_doc_data(
            supabase=request.app.state.supabase_client,
            user_id=user_id,
        )
        activities = await get_activities_by_user_id(
            supabase=request.app.state.supabase_client,
            user_id=user_id,
        )

        activities_by_category = defaultdict(list)
        for a in activities:
            activities_by_category[a.category].append(a)

        brag_doc.activities_by_category = activities_by_category

        return brag_doc
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


update_brag_doc_endpoint = "/api-v1/brag-doc/updateBragDoc/"
@app.post(update_brag_doc_endpoint)
async def update_brag_doc_for_user(brag_doc_update_request: BragDocUpdateRequest, request: Request):
    logger.debug(f"New request to {update_brag_doc_endpoint} endpoint")
    try:
        if brag_doc_update_request.url:
            brag_doc_update_request.url = brag_doc_update_request.url.strip()

        brag_doc: BragDoc = await get_brag_doc_data(
            supabase=request.app.state.supabase_client,
            user_id=brag_doc_update_request.user_id
        )
        if not brag_doc.brag_doc_id:
            await create_brag_doc(
                supabase=request.app.state.supabase_client,
                update_request=brag_doc_update_request,
            )
        else:
            await update_brag_doc(
                supabase=request.app.state.supabase_client,
                update_request=brag_doc_update_request,
            )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


create_activities_from_check_in_endpoint = "/api-v1/brag-doc/createActivitiesFromCheckIn/"
@app.post(create_activities_from_check_in_endpoint)
async def create_tasks_from_check_in(check_in: CheckIn, request: Request):
    logger.debug(f"New request to {create_activities_from_check_in_endpoint} endpoint")
    try:
        activities: List[Activity] = create_activities_from_check_in(
            check_in=check_in,
            state=request.app.state)
        return activities
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(app)
