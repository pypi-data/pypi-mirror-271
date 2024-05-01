from uuid import UUID

from pydantic import BaseModel


class UserCompactResp(BaseModel):
    id: UUID
    full_name: str
    email: str
