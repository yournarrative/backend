from typing import List

from postgrest import APIResponse
from supabase import Client

from information_retrieval.api.api_v1.model.activity import Activity
from information_retrieval.api.api_v1.model.brag_doc import BragDoc, BragDocUpdateRequest
from information_retrieval.api.api_v1.model.users import NarrativeUser
from information_retrieval.utils.other import generate_random_string
from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


async def get_user_email_by_id(supabase: Client, user_id: str) -> NarrativeUser:
    logger.debug(f"Getting all documents for user: {user_id}")
    try:
        response: APIResponse = (
            supabase
                .table("profiles")
                .select("id, email")
                .eq("id", user_id)
                .execute()
        )
        user = NarrativeUser(id=response.data[0].get("id"),
                             email=response.data[0].get("email"))
        return user
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def get_activities_by_user_id(supabase: Client, user_id: str) -> List[Activity]:
    logger.debug(f"Getting all documents for user: {user_id}")
    try:
        response: APIResponse = (
            supabase
                .table("activities")
                .select("id, title, description, category, status")
                .eq("user_id", user_id)
                .execute()
        )

        activities = []
        for r in response.data:
            activities.append(
                Activity(id=r.get("id"),
                         title=r.get("title"),
                         description=r.get("description"),
                         category=r.get("category"),
                         status=r.get("status"))
            )
        return activities
    except Exception as e:
        logger.error(f"Error getting all documents for user: {user_id}, error: {e}")
        raise e


async def insert_new_user_activities(supabase: Client, user_id: str, activities: List[Activity]):
    logger.debug(f"Inserting new activities for user_id: {user_id}, activities: {activities}")
    # TODO: Validate that category, status columns are valid
    try:
        data_to_upsert = []
        for activity in activities:
            d = dict(activity)
            d['user_id'] = user_id
            data_to_upsert.append(d)

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


async def is_brag_doc_url_taken(supabase: Client, url: str) -> bool:
    logger.debug(f"Checking if brag doc url is taken: {url}")
    try:
        response: APIResponse = (
            supabase
                .table('brag_docs')
                .select('url')
                .eq('url', url.strip())
                .execute()
        )
        return bool(response.data)
    except Exception as e:
        logger.error(f"Error checking if brag doc url is taken: {url}, error: {e}")
        raise e


async def get_brag_doc_data(supabase: Client, user_id: str) -> BragDoc:
    logger.debug(f"Getting brag doc for user: {user_id}")
    try:
        response: APIResponse = (
            supabase
                .table('brag_docs')
                .select('user_id, url, data, id')
                .eq('user_id', user_id)
                .execute()
        )
        unpack = response.data[0] if response.data else {}
        brag_doc = BragDoc(user_id=unpack.get("user_id", ""),
                           url=unpack.get("url", ""),
                           published=unpack.get("data", {}).get("published", False),
                           brag_doc_id=unpack.get("id", ""),)
        return brag_doc
    except Exception as e:
        logger.error(f"Error getting brag doc for user: {user_id}, error: {e}")
        raise e


async def create_brag_doc(supabase: Client, update_request: BragDocUpdateRequest) -> None:
    logger.debug(f"Creating brag doc for user: {update_request.user_id}")

    d = {
        "user_id": update_request.user_id,
        "data": {"published": update_request.publish},
        "url": update_request.url if update_request.url else generate_random_string(16),
    }

    try:
        while True:
            if await is_brag_doc_url_taken(supabase, d.get("url")):
                d["url"] = generate_random_string(16)
                continue

            else:
                response: APIResponse = (
                    supabase
                        .table('brag_docs')
                        .insert(d)
                        .execute()
                )
                break

    except Exception as e:
        logger.error(f"Error checking if url exists, error: {e}")
        raise e


async def update_brag_doc(supabase: Client, update_request: BragDocUpdateRequest) -> None:
    logger.debug(f"Updating brag doc for user: {update_request.user_id}")

    d = {
        "data": {"published": update_request.publish},
        "url": update_request.url,
    }

    try:
        response: APIResponse = (
            supabase
                .table('brag_docs')
                .update(d)
                .eq('user_id', update_request.user_id)
                .execute()
        )
    except Exception as e:
        logger.error(f"Error updating brag doc for user: {update_request.user_id}, error: {e}")
        raise e
