from collections import defaultdict

from fastapi import APIRouter, HTTPException, Request, Response

from information_retrieval.api.api_v1.ai_processing.check_in import create_activities_from_check_in_ai
from information_retrieval.api.api_v1.model.activity import Activity
from information_retrieval.api.api_v1.model.brag_doc import BragDoc, BragDocUpdateRequest
from information_retrieval.api.api_v1.model.checkin import CheckIn
from information_retrieval.connectors.supabase.crud import (
    create_brag_doc,
    get_activities_by_user_id,
    get_brag_doc_data,
    update_brag_doc,
)
from information_retrieval.utils.standard_logger import app_logger as logger

router = APIRouter()


get_brag_doc_endpoint = "/api-v1/brag-doc/getBragDocForUser/{user_id}"


@router.get(get_brag_doc_endpoint)
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


@router.post(update_brag_doc_endpoint)
async def update_brag_doc_for_user(brag_doc_update_request: BragDocUpdateRequest, request: Request):
    logger.debug(f"New request to {update_brag_doc_endpoint} endpoint")
    try:
        if brag_doc_update_request.url:
            brag_doc_update_request.url = brag_doc_update_request.url.strip()

        brag_doc: BragDoc = await get_brag_doc_data(
            supabase=request.app.state.supabase_client, user_id=brag_doc_update_request.user_id
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


@router.post(create_activities_from_check_in_endpoint)
async def create_tasks_from_check_in(check_in: CheckIn) -> list[Activity]:
    logger.debug(f"New request to {create_activities_from_check_in_endpoint} endpoint")
    try:
        activities: list[Activity] = create_activities_from_check_in_ai(check_in=check_in)
        return activities
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
