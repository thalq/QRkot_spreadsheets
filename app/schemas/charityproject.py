from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]

    @validator('name', 'description', 'full_amount')
    def none_and_empty_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError('Все поля обязательны. "" или None не допускаются.')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectUpdate):
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
