from typing import List, Dict

from cohere.responses import Chat
from starlette.datastructures import State

from information_retrieval.api.api_v1.model.document import RetrieveDocument
from information_retrieval.api.api_v1.model.query import RAGResponse
from information_retrieval.utils.standard_logger import get_logger


logger = get_logger()


async def RAG_query(user_email: str, query: str, documents: List[RetrieveDocument], state: State) -> RAGResponse:
    logger.debug(f"Searching {user_email}'s documents with query {query}...")

    # i = 0
    formatted_docs: List[Dict] = []
    for d in documents:
        f = {
            # "title": f"Fake title {i}",
            "snippet": d.content
        }
        formatted_docs.append(f)
        # i += 1

    try:
        logger.debug(f"Sending query to Cohere API...")
        response: Chat = state.cohere_client.chat(
            model="command",
            message=query,
            documents=formatted_docs,
            prompt_truncation='AUTO'
        )
        logger.debug(f"Successfully fetched response from Cohere API.")

    except Exception as e:
        logger.error(f"Error fetching response from Cohere API, error: {e}")
        raise e

    # Wrapping in try/catch in case cohere response format changes
    # Could do more elegantly with key checks
    try:
        rag_response = RAGResponse(
            user_email=user_email,
            query=query,
            response=response.text,
            citations=response.citations,
            documents=response.documents,
        )
    except Exception as e:
        logger.error(f"Error parsing response from Cohere API: {response}, error: {e}")
        raise e

    return rag_response
