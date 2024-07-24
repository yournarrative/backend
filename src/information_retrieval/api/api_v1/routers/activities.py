from fastapi import APIRouter, HTTPException, Request, Response

from information_retrieval.api.api_v1.ai_processing.update_existing_activity import update_activity_with_new_details_ai
from information_retrieval.api.api_v1.model.activity import ActivityWithID, InsertActivitiesForUserRequest
from information_retrieval.connectors.supabase.crud import (
    get_activities_by_user_id,
    get_activity_details_by_id,
    insert_new_user_activities,
    upsert_activity_by_id,
)
from information_retrieval.utils.standard_logger import app_logger as logger

router = APIRouter()


insert_activities_endpoint = "/api-v1/activities/insertActivities/"


@router.post(insert_activities_endpoint)
async def insert_activities(data: InsertActivitiesForUserRequest, request: Request):
    logger.debug(f"New request to {insert_activities_endpoint} endpoint")
    try:
        await insert_new_user_activities(
            supabase=request.app.state.supabase_client, user_id=data.user_id, activities=data.activities
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


get_activities_endpoint = "/api-v1/activities/getActivitiesForUser/{user_id}"


@router.get(get_activities_endpoint)
async def get_activities_for_user(user_id: str, request: Request) -> list[ActivityWithID]:
    logger.debug(f"New request to {get_activities_endpoint} endpoint")
    try:
        activities: list[ActivityWithID] = await get_activities_by_user_id(
            supabase=request.app.state.supabase_client,
            user_id=user_id,
        )
        return activities
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


upsert_activity_endpoint = "/api-v1/activities/upsertActivity/"


@router.post(upsert_activity_endpoint)
async def update_activity(activity_with_id: ActivityWithID, request: Request):
    logger.debug(f"New request to {upsert_activity_endpoint} endpoint")
    try:
        await upsert_activity_by_id(
            supabase=request.app.state.supabase_client,
            activity_with_id=activity_with_id,
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


update_activity_with_new_details_endpoint = "/api-v1/activities/updateActivityWithNewDetails/"


async def update_activity_with_new_details(activity_id: str, new_details: str, request: Request) -> ActivityWithID:
    # TODO: Take User ID and pass into get_activity_details_by_id to check if user owns activity

    logger.debug(f"New request to {update_activity_with_new_details_endpoint} endpoint")

    # Get activity details by id
    try:
        activity_with_id: ActivityWithID = await get_activity_details_by_id(
            supabase=request.app.state.supabase_client,
            activity_id=activity_id,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

    # Update activity with new details
    try:
        updated_activity_with_id: ActivityWithID = update_activity_with_new_details_ai(
            activity_with_id=activity_with_id,
            update=new_details,
        )
        return updated_activity_with_id
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
