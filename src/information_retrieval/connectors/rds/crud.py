from typing import List, Dict, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from information_retrieval.api.api_v1.model.document import RetrieveDocument
from information_retrieval.utils.standard_logger import get_logger


logger = get_logger()


async def insert_new_document(
        async_session: AsyncSession,
        user_email: str,
        content: str,
        question: str,
        document_type: str,
) -> None:
    logger.debug(f"Inserting document for user email {user_email}...")
    query = text(
        f"""
        INSERT INTO documents(
            user_id,
            content,
            question,
            document_type
        )
        VALUES
        ((SELECT id FROM users WHERE email = '{user_email}' LIMIT 1), '{content}','{question}', '{document_type}')"""
    )
    async with async_session as session:
        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            logger.error(f"Error uploading document for user email {user_email}, error: {e}")
            await session.rollback()
            raise e
        else:
            logger.debug(f"Successfully uploaded document for {user_email}.")


async def get_all_documents_from_user(async_session: AsyncSession, user_email: str) -> List[RetrieveDocument]:
    logger.debug(f"Getting all documents from user {user_email}...")

    async with async_session as session:
        query = text(
            f"""
            SELECT documents.content 
            FROM documents
                JOIN users 
                    ON documents.user_id = users.id
            WHERE users.email = '{user_email}'
            ORDER BY documents.created_on DESC;
            """
        )
        resp: List[Tuple] = (await session.execute(query)).fetchall()
        docs: List[RetrieveDocument] = [RetrieveDocument(content=r[0]) for r in resp]
        logger.debug(f"Successfully retrieved {len(docs)} for user {user_email}.")
    return docs
