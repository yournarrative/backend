# import cohere
# from cohere.responses import Chat
#
# from information_retrieval.core.logger import app_logger as logger
#
# DOC_LIMIT = 20
#
#
# async def rag_query(cohere_client: cohere.Client, query: str, documents: list[dict]) -> str:
#     logger.debug("Starting RAG query with Cohere Client...")
#
#     formatted_docs: list[dict] = []
#     for d in documents[:DOC_LIMIT]:
#         f = {
#             "title": d.get("title", ""),
#             "description": d.get("description", ""),
#             "status": d.get("status", ""),
#         }
#         formatted_docs.append(f)
#
#     logger.debug("Sending query to Cohere API...")
#     try:
#         response: Chat = cohere_client.chat(
#             model="command", message=query, documents=formatted_docs, prompt_truncation="AUTO"
#         )
#     except Exception as e:
#         logger.error(f"Error fetching response from Cohere API, error: {e}")
#         raise e
#
#     else:
#         logger.debug("Successfully fetched response from Cohere API.")
#         return response.text
