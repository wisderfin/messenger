from pydantic import BaseModel


class BaseScheme(BaseModel):  # TODO: reading a documentation for it
    class Config:
        from_attributes = True
