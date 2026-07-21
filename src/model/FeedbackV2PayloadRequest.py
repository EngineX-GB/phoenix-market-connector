from pydantic import BaseModel


class FeedbackV2PayloadRequest(BaseModel):
    user_id : str
    records : list[str]