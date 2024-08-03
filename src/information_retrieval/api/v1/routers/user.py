from fastapi import APIRouter, HTTPException, Request

from information_retrieval.api.v1.models.user import GetUserDataRequest, GetUserDataResponse, NarrativeUser
from information_retrieval.connectors.supabase.crud import get_user_email_by_id
from information_retrieval.core.logger import app_logger as logger

router = APIRouter()


get_user_data_endpoint = "/v1/users/getUserData/"


@router.post(get_user_data_endpoint)
async def get_user_data(data: GetUserDataRequest, request: Request) -> GetUserDataResponse:
    logger.debug(f"New request to {get_user_data_endpoint} endpoint: {data}")
    try:
        user_data: NarrativeUser = await get_user_email_by_id(request.app.state.supabase_client, data.user_id)
        return GetUserDataResponse(user_data=user_data)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
