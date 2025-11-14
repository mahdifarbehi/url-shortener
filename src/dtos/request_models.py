from pydantic import BaseModel


class CreateShortLinkRequestModel(BaseModel):
    original_url: str
