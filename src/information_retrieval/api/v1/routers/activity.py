from fastapi import APIRouter, HTTPException, Request, Response

from information_retrieval.api.v1.models.activity import (
    Activity,
    ActivityWithID,
    CreateActivitiesFromCheckInRequest,
    CreateActivitiesFromCheckInResponse,
    DeleteActivitiesRequest,
    GetActivitiesAISummaryRequest,
    GetActivitiesAISummaryResponse,
    GetActivitiesRequest,
    GetActivitiesResponse,
    InsertActivitiesForUserRequest,
    UpdateActivityWithNewDetailsRequest,
    UpdateActivityWithNewDetailsResponse,
    UpsertActivityRequest,
)
from information_retrieval.api.v1.processing.ai.activity_list_to_summary import create_summary_from_activities_ai
from information_retrieval.api.v1.processing.ai.check_in_to_activities import create_activities_from_check_in_ai
from information_retrieval.api.v1.processing.ai.update_existing_activity import update_activity_with_new_details_ai
from information_retrieval.connectors.supabase.crud import (
    get_activities_by_user_id,
    get_activity_details_by_id,
    insert_new_user_activities,
    soft_delete_activities_by_id,
    upsert_activity_by_id,
)
from information_retrieval.core.logger import app_logger as logger

router = APIRouter()


insert_activities_endpoint = "/v1/activities/insertActivities/"


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


delete_activities_endpoint = "/v1/activities/deleteActivities/"


@router.post(delete_activities_endpoint)
async def delete_activities(data: DeleteActivitiesRequest, request: Request):
    logger.debug(f"New request to {delete_activities_endpoint} endpoint")
    try:
        await soft_delete_activities_by_id(
            supabase=request.app.state.supabase_client,
            activity_id_list=data.activity_id_list,
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


get_activities_endpoint = "/v1/activities/getActivities/"


@router.post(get_activities_endpoint)
async def get_activities(data: GetActivitiesRequest, request: Request) -> GetActivitiesResponse:
    logger.debug(f"New request to {get_activities_endpoint} endpoint")
    try:
        activities: list[ActivityWithID] = await get_activities_by_user_id(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
        )
        return GetActivitiesResponse(user_id=data.user_id, activities=activities)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


upsert_activity_endpoint = "/v1/activities/upsertActivity/"


@router.post(upsert_activity_endpoint)
async def update_activity(data: UpsertActivityRequest, request: Request):
    logger.debug(f"New request to {upsert_activity_endpoint} endpoint")
    try:
        await upsert_activity_by_id(
            supabase=request.app.state.supabase_client,
            activity_with_id=data.activity_with_id,
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


update_activity_with_new_details_endpoint = "/v1/activities/updateActivityWithNewDetails/"


@router.post(update_activity_with_new_details_endpoint)
async def update_activity_with_new_details(
    data: UpdateActivityWithNewDetailsRequest, request: Request
) -> UpdateActivityWithNewDetailsResponse:
    # TODO: Take User ID and pass into get_activity_details_by_id to check if user owns activity

    logger.debug(f"New request to {update_activity_with_new_details_endpoint} endpoint")

    # Get activity details by id
    try:
        activity_with_id: ActivityWithID = await get_activity_details_by_id(
            supabase=request.app.state.supabase_client,
            activity_id=data.activity_id,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

    # Update activity with new details
    try:
        updated_activity_with_id: ActivityWithID = update_activity_with_new_details_ai(
            activity_with_id=activity_with_id,
            update=data.update,
        )
        return UpdateActivityWithNewDetailsResponse(activity_with_id=updated_activity_with_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


create_activities_from_check_in_endpoint = "/v1/activities/createActivitiesFromCheckIn/"


@router.post(create_activities_from_check_in_endpoint)
async def create_activities_from_check_in(
    data: CreateActivitiesFromCheckInRequest,
) -> CreateActivitiesFromCheckInResponse:
    logger.debug(f"New request to {create_activities_from_check_in_endpoint} endpoint")
    try:
        activities: list[Activity] = create_activities_from_check_in_ai(dialogue=data.dialogue)
        return CreateActivitiesFromCheckInResponse(activities=activities)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


get_ai_summary_for_activities_endpoint = "/v1/activities/getAISummaryForActivities/"


@router.post(get_ai_summary_for_activities_endpoint)
async def get_ai_summary_for_activities(data: GetActivitiesAISummaryRequest):
    logger.debug(f"New request to {get_ai_summary_for_activities_endpoint} endpoint")
    try:
        summary: str = create_summary_from_activities_ai(activities=data.activities)
        return GetActivitiesAISummaryResponse(summary=summary)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
