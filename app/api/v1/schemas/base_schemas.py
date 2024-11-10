from pydantic import BaseModel


class BaseSchema(BaseModel):  # TODO: reading a documentation for it
    class Config:
        from_attributes = True
