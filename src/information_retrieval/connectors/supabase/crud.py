from httpx import Response
from postgrest import APIResponse
from supabase import Client

from information_retrieval.api.v1.models.activity import Activity, ActivityWithID
from information_retrieval.api.v1.models.user import NarrativeUser
from information_retrieval.core.logger import app_logger as logger


async def get_user_profile_data_by_id(supabase: Client, user_id: str) -> NarrativeUser:
    logger.debug(f"Getting all profile data for user: {user_id}")
    try:
        response: APIResponse = supabase.table("profiles").select("*").eq("id", user_id).execute()
        user = NarrativeUser(
            user_id=response.data[0].get("id"),
            email=response.data[0].get("email"),
            phone_number=response.data[0].get("phone_number", None),
            bio=response.data[0].get("bio", None),
            linkedin_profile_url=response.data[0].get("linkedin_profile_url", None),
            current_organization=response.data[0].get("current_organization", None),
            loom_url=response.data[0].get("loom_url", None),
        )
        return user
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def update_user_profile_data_by_id(supabase: Client, user: NarrativeUser):
    logger.debug(f"Updating user profile for user_id: {user.user_id}")

    user_data_dict = user.dict()
    del user_data_dict["user_id"]

    try:
        _, _ = supabase.table("profiles").update(user_data_dict).eq("id", user.user_id).execute()
    except Exception as e:
        logger.error(f"Error updating user profile for user_id: {user.user_id}, error: {e}")
        raise e
    else:
        logger.debug(f"Successfully updated user profile for id: {user.user_id} to {user}")


async def get_all_organizations_for_user_by_id(supabase: Client, user_id: str) -> list[str]:
    logger.debug(f"Getting all organizations for user: {user_id}")
    try:
        response: APIResponse = (
            supabase.table("activities").select("organization").eq("user_id", user_id).eq("deleted", False).execute()
        )

        organizations = []
        for r in response.data:
            organizations.append(r.get("organization"))
        return organizations
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def get_activities_by_user_id(supabase: Client, user_id: str) -> list[ActivityWithID]:
    logger.debug(f"Getting all activities for user: {user_id}")
    try:
        response: APIResponse = (
            supabase.table("activities")
            .select("id, title, description, category, status, organization")
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
                    organization=r.get("organization", None),
                )
            )
        return activities
    except Exception as e:
        logger.error(f"Error getting all activities for user: {user_id}, error: {e}")
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

        _, _ = supabase.table("activities").upsert(data_to_upsert).execute()
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
            organization=r.get("organization", None),
        )
        return activity_with_id
    except Exception as e:
        logger.error(f"Error getting activity details for activity_id: {activity_id}, error: {e}")
        raise e


async def get_activities_grouped_by_organization(supabase: Client, user_id: str) -> dict[str, list[ActivityWithID]]:
    logger.debug(f"Getting activities grouped by organization for user: {user_id}")
    try:
        response: APIResponse = (
            supabase.table("activities")
            .select("id, title, description, category, status, organization")
            # .eq("user_id", user_id)
            .eq("deleted", False)
            .execute()
        )

        activities_grouped_by_organization = {}
        for r in response.data:
            organization = r.get("organization", None)

            if organization is None or organization == "":
                organization = "Personal"

            if organization not in activities_grouped_by_organization:
                activities_grouped_by_organization[organization] = []

            activities_grouped_by_organization[organization].append(
                ActivityWithID(
                    id=r.get("id"),
                    title=r.get("title"),
                    description=r.get("description"),
                    category=r.get("category"),
                    status=r.get("status"),
                    organization=r.get("organization", None),
                )
            )
        return activities_grouped_by_organization
    except Exception as e:
        logger.error(f"Error getting activities grouped by organization for user: {user_id}, error: {e}")
        raise e


async def upsert_file_to_object_storage(
    supabase: Client, user_id: str, bucket_name: str, file_name: str, file_content: bytes, file_content_type: str
):
    file_name = f"{user_id}/{file_name}"
    try:
        response: Response = supabase.storage.from_(bucket_name).upload(
            path=file_name, file=file_content, file_options={"upsert": "true", "content-type": file_content_type}
        )
        if response.status_code != 200:
            raise Exception(f"File upsert response - {response.status_code}; {response.text}")
    except Exception as e:
        logger.error(f"Failed to upsert file {file_name} to bucket {bucket_name}: {e}")
        raise e


async def get_file_from_object_storage(supabase: Client, user_id: str, bucket_name: str, file_name: str) -> bytes:
    file_name = f"{user_id}/{file_name}"
    try:
        content: bytes = supabase.storage.from_(bucket_name).download(file_name)
    except Exception as e:
        logger.error(f"Failed to download file {file_name} from bucket {bucket_name}: {e}")
        raise e
    else:
        return content
