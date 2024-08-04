from fastapi import APIRouter, HTTPException, Request, Response

from information_retrieval.api.v1.models.user import (
    GetAllOrganizationsForUserRequest,
    GetAllOrganizationsForUserResponse,
    GetUserProfileDataRequest,
    GetUserProfileDataResponse,
    NarrativeUser,
    UpdateUserProfileDataRequest,
)
from information_retrieval.connectors.supabase.crud import (
    get_all_organizations_for_user_by_id,
    get_user_profile_data_by_id,
    update_user_profile_data_by_id,
)
from information_retrieval.core.logger import app_logger as logger

router = APIRouter()


get_user_profile_data_endpoint = "/v1/users/getUserProfileData/"


@router.post(get_user_profile_data_endpoint)
async def get_user_data(data: GetUserProfileDataRequest, request: Request) -> GetUserProfileDataResponse:
    logger.debug(f"New request to {get_user_profile_data_endpoint} endpoint: {data}")

    try:
        user_data: NarrativeUser = await get_user_profile_data_by_id(request.app.state.supabase_client, data.user_id)
        return GetUserProfileDataResponse(user_data=user_data)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


update_user_profile_data_endpoint = "/v1/users/updateUserProfileData/"


@router.post(update_user_profile_data_endpoint)
async def update_user_data(data: UpdateUserProfileDataRequest, request: Request):
    logger.debug(f"New request to {update_user_profile_data_endpoint} endpoint: {data}")

    try:
        await update_user_profile_data_by_id(request.app.state.supabase_client, data.user_data)
        return Response(status_code=200)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


get_all_organizations_for_user_endpoint = "/v1/activities/getAllOrganizationsForUser/"


@router.post(get_all_organizations_for_user_endpoint)
async def get_all_organizations_for_user(
    data: GetAllOrganizationsForUserRequest, request: Request
) -> GetAllOrganizationsForUserResponse:
    logger.debug(f"New request to {get_all_organizations_for_user_endpoint} endpoint: {data}")

    try:
        organizations: list[str] = await get_all_organizations_for_user_by_id(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
        )
        organizations = list(set(filter(lambda x: x is not None, organizations)))
        return GetAllOrganizationsForUserResponse(organizations=organizations)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
