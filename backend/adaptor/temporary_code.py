from pydantic import BaseModel


class TemporaryCode(BaseModel):
    code: str
