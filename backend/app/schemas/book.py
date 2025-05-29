from pydantic import BaseModel,Field ,HttpUrl , field_validator , model_validator
from typing import Optional

class BookCreate(BaseModel):
    name: str = Field(..., min_length=1,max_length=255)
    link: HttpUrl
    description: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('name')
    def name_must_contian_text(cls, v):
        if not v.isalpha():
            raise ValueError('name must contain only letters')
        return v
    class Config:
        from_attributes = True

class BookRead(BaseModel):
    id: int
    name: str
    link: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    
    @model_validator(mode="after")
    def check_at_least_one_field(cls, values):
        if all(v is None for v in values.model_dump().values()):
            raise ValueError("At least one field must be provided")
        return values

    class Config:
        from_attributes = True

class BookBasicInfo(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True