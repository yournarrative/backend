from postgrest import APIResponse
from supabase import Client

from information_retrieval.api.v1.model.activities import Activity, ActivityWithID
from information_retrieval.api.v1.model.users import NarrativeUser
from information_retrieval.core.logger import app_logger as logger


async def get_user_email_by_id(supabase: Client, user_id: str) -> NarrativeUser:
    logger.debug(f"Getting all documents for user: {user_id}")
    try:
        response: APIResponse = supabase.table("profiles").select("id, email").eq("id", user_id).execute()
        user = NarrativeUser(user_id=response.data[0].get("id"), email=response.data[0].get("email"))
        return user
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def get_activities_by_user_id(supabase: Client, user_id: str) -> list[ActivityWithID]:
    logger.debug(f"Getting all documents for user: {user_id}")
    try:
        response: APIResponse = (
            supabase.table("activities")
            .select("id, title, description, category, status")
            .eq("user_id", user_id)
            .eq("deleted", False)
            .execute()
        )

        activities = []
        for r in response.data:
            activities.append(
                ActivityWithID(
                    id=r.get("id"),
                    title=r.get("title"),
                    description=r.get("description"),
                    category=r.get("category"),
                    status=r.get("status"),
                )
            )
        return activities
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def upsert_activity_by_id(supabase: Client, activity_with_id: ActivityWithID):
    logger.debug(f"Updating activity for activity_id: {activity_with_id.id}")
    try:
        _, _ = supabase.table("activities").update(activity_with_id.dict()).eq("id", activity_with_id.id).execute()
    except Exception as e:
        logger.error(f"Error updating activity for activity_id: {activity_with_id.id}, error: {e}")
        raise e
    else:
        logger.debug(f"Successfully updated activity_id: {activity_with_id.id} to {activity_with_id}")


async def insert_new_user_activities(supabase: Client, user_id: str, activities: list[Activity]):
    logger.debug(f"Inserting new activities for user_id: {user_id}, activities: {activities}")
    # TODO: Validate that category, status columns are valid
    try:
        data_to_upsert = []
        for activity in activities:
            d = dict(activity)
            d["user_id"] = user_id
            data_to_upsert.append(d)

        data, count = supabase.table("activities").upsert(data_to_upsert).execute()
    except Exception as e:
        logger.error(f"Error uploading activities for user: {user_id}, error: {e}")
        raise e
    else:
        logger.debug(f"Successfully uploaded {len(activities)} activities for user: {user_id}")


async def soft_delete_activities_by_id(supabase: Client, activity_id_list: list[str]):
    logger.debug(f"Soft deleting activities: {activity_id_list}")
    try:
        _, _ = supabase.table("activities").update({"deleted": True}).in_("id", activity_id_list).execute()
    except Exception as e:
        logger.error(f"Error soft deleting activities for activity_ids: {activity_id_list}, error: {e}")
        raise e
    else:
        logger.debug(f"Successfully soft deleted activity_ids: {activity_id_list}")


async def get_activity_details_by_id(supabase: Client, activity_id: str) -> ActivityWithID:
    # TODO get user id too and validate they own this activity?

    logger.debug(f"Getting activity details for activity_id: {activity_id}")
    try:
        response: APIResponse = (
            supabase.table("activities")
            .select("id, title, description, category, status")
            .eq("id", activity_id)
            .eq("deleted", False)
            .execute()
        )

        r = response.data[0]

        if not response.data or not response.data[0]:
            raise Exception(f"Activity with id: {activity_id} not found or soft deleted")

        activity_with_id = ActivityWithID(
            id=r.get("id"),
            title=r.get("title"),
            description=r.get("description"),
            category=r.get("category"),
            status=r.get("status"),
        )
        return activity_with_id
    except Exception as e:
        logger.error(f"Error getting activity details for activity_id: {activity_id}, error: {e}")
        raise e
