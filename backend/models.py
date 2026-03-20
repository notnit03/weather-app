from pydantic import BaseModel
from typing import Optional

class WeatherRecordCreate(BaseModel):
    location: str
    date_from: str
    date_to: str

class WeatherRecordUpdate(BaseModel):
    location: Optional[str] = None
    temperature: Optional[float] = None
    description: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None

class WeatherRecordResponse(BaseModel):
    id: int
    location: str
    temperature: float
    description: str
    date_from: str
    date_to: str

    class Config:
        from_attributes = True