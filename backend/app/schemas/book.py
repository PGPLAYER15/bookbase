from pydantic import BaseModel,Field ,HttpUrl , field_validator , model_validator
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1,max_length=255)
    link: HttpUrl
    description: Optional[str] = Field(None, max_length=1000)
    author: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    
    @field_validator('title')
    def name_must_contian_text(cls, v):
        if not all(c.isalnum() or c.isspace() or c in ".,;:¿?¡!-_()" for c in v):
            raise ValueError('El título contiene caracteres no permitidos')
        return v

    @model_validator(mode='after')
    def convert_link_to_str(self):
        if isinstance(self.link, HttpUrl):
            self.link = str(self.link)
        return self

    class Config:
        from_attributes = True

class BookRead(BaseModel):
    id: int
    title: str
    link: Optional[HttpUrl] = None
    description: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    link: Optional[HttpUrl] = None
    description: Optional[str] = Field(None, max_length=1000)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    
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