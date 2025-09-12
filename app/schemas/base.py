from pydantic import BaseModel

class SchemaBase(BaseModel):
    class Config:
        orm_mode = True
