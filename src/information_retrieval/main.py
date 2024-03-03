from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from information_retrieval.api.api_v1.model.document import InsertDocument, RetrieveDocument
from information_retrieval.api.api_v1.model.query import Query, RAGResponse
from information_retrieval.app_lifespan_management import init_app_state, cleanup_app_state
from information_retrieval.connectors.cohere.crud import RAG_query
from information_retrieval.connectors.rds.crud import get_all_documents_from_user, insert_new_document
from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app_state(app.state)
    yield
    await cleanup_app_state(app.state)


app = FastAPI(title="Ghosted", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


@app.post("/api-v1/insert/insertDocument/")
async def insert_document(data: InsertDocument, request: Request):
    try:
        await insert_new_document(
            async_session=request.app.state.database_access_layer.async_session,
            user_email=data.user_email,
            content=data.content,
            question=data.question,
            document_type=data.document_type,
        )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/query/queryUserHistory/")
async def query_user_history(data: Query, request: Request):
    try:
        docs: List[RetrieveDocument] = await get_all_documents_from_user(
            async_session=request.app.state.database_access_layer.async_session,
            user_email=data.user_email,
        )
        response: RAGResponse = await RAG_query(
            user_email=data.user_email,
            query=data.query,
            documents=docs,
            state=request.app.state
        )
        return response
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(app)
