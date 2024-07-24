from fastapi import APIRouter, HTTPException, Request

from information_retrieval.api.api_v1.model.users import NarrativeUser
from information_retrieval.connectors.supabase.crud import get_user_email_by_id
from information_retrieval.utils.standard_logger import app_logger as logger

router = APIRouter()


get_users_endpoint = "/api-v1/users/getUserInformation/{user_id}"


@router.get(get_users_endpoint)
async def get_user_data(user_id: str, request: Request) -> NarrativeUser:
    logger.debug(f"New request to {get_users_endpoint} endpoint")
    try:
        user: NarrativeUser = await get_user_email_by_id(request.app.state.supabase_client, user_id)
        return user

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
