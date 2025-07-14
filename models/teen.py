from pydantic import BaseModel, Field
from pydantic import PlainValidator, WithJsonSchema
from bson import ObjectId
from typing import Optional, Literal, Annotated


# --------- ObjectId validator + JSON schema ---------
def validate_object_id(v):
    if isinstance(v, ObjectId):
        return v
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return ObjectId(v)

# Annotated type that validates and generates JSON Schema as a string with regex for ObjectId
ObjectIdType = Annotated[
    ObjectId,
    PlainValidator(validate_object_id),
    WithJsonSchema({"type": "string", "pattern": "^[a-fA-F0-9]{24}$", "examples": ["507f1f77bcf86cd799439011"]})
]


# ---------- Teen Model ----------
class TeenModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    teen_id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    location: Optional[str] = None
    school_grade: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {str: str}


# ---------- Phone Usage Model ----------
class PhoneUsageModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    usage_id: Optional[int] = None
    teen_id: str  # Reference to Teen's ObjectId as a string
    daily_usage_hours: Optional[float] = None
    sleep_hours: Optional[float] = None
    phone_checks_per_day: Optional[int] = None
    screen_time_before_bed: Optional[float] = None
    weekend_usage_hours: Optional[float] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {str: str}


# ---------- Mental Health Model ----------
class MentalHealthModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ObjectId as string
    stats_id: Optional[int] = None
    teen_id: str  # Referencing Teen's _id, stored as ObjectId in Mongo, returned as string
    anxiety_level: Optional[int] = None
    depression_level: Optional[int] = None
    self_esteem: Optional[int] = None
    parental_control: Optional[int] = None
    family_communication: Optional[int] = None
    addiction_level: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {str: str}


# ---------- App Usage Model ----------
class AppUsageModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ObjectId as string
    appusage_id: Optional[int] = None
    teen_id: str  # ObjectId stored as string
    time_on_social_media: Optional[float] = None
    time_on_gaming: Optional[float] = None
    time_on_education: Optional[float] = None
    apps_used_daily: Optional[int] = None
    phone_usage_purpose: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {str: str}
