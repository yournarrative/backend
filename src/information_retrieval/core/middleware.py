from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if self._is_post_with_file_upload(request):
            content_length = request.headers.get("Content-Length")
            if self._is_content_length_exceeded(content_length, request):
                return JSONResponse(status_code=413, content={"detail": "File too large"})

        return await call_next(request)

    def _is_post_with_file_upload(self, request: Request) -> bool:
        return (
            request.method == "POST"
            and request.headers.get("Content-Type", "").startswith("multipart/form-data")
            and "Content-Length" in request.headers
        )

    def _is_content_length_exceeded(self, content_length: str, request: Request) -> bool:
        if content_length is None:
            return False
        max_file_size = int(request.app.state.settings.config.get("MAX_FILE_SIZE"))
        return int(content_length) > max_file_size
