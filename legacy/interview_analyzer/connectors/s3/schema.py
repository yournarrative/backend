from pydantic import BaseModel


class ProcessS3Request(BaseModel):
    bucket: str
    key: str
    send_email_when_finished: bool = False
