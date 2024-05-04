from typing import List

from postgrest import APIResponse
from supabase import Client

from information_retrieval.api.api_v1.model.activity import Activity
from information_retrieval.api.api_v1.model.users import NarrativeUser
from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


async def get_user_by_id(supabase: Client, user_id: str) -> NarrativeUser:
    logger.debug(f"Getting all documents for user: {user_id}")
    try:
        response: APIResponse = (
            supabase
                .table("users")
                .select("data->first_name, data->last_name, email")
                .eq("id", user_id)
                .execute()
        )
        user = NarrativeUser(first_name=response.data[0].get("first_name"),
                             last_name=response.data[0].get("last_name"),
                             email=response.data[0].get("email"))
        return user
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def insert_new_user_activity(supabase: Client, user_id: str, activities: List[Activity]):
    logger.debug(f"Inserting new activity - user_id: {user_id}, activities: {activities}")
    # TODO: Validate that category, status columns are valid
    try:
        data_to_upsert = [dict(activity) for activity in activities]
        data, count = (
            supabase
                .table("activities")
                .upsert(data_to_upsert)
                .execute()
        )
    except Exception as e:
        logger.error(f"Error uploading activities for user: {user_id}, error: {e}")
        raise e
    else:
        logger.debug(f"Successfully uploaded {count} activities for user: {user_id}")
