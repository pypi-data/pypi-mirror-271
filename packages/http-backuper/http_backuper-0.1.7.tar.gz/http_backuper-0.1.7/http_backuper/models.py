from enum import Enum
from typing import List, Dict
from typing import Optional

from pydantic import BaseModel, HttpUrl, validator, AnyUrl


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Frequency(str, Enum):
    MINUTE = "minutes"
    HOUR = "hours"
    DAY = "days"
    WEEK = "weeks"


class Source(BaseModel):
    name: str
    path: Optional[str]
    command: Optional[str]
    container_name: Optional[str]

    @validator("path", "command", pre=True)
    def check_path_and_command(cls, value, values, **kwargs):
        if "path" in values and "command" in values:
            raise ValueError("Path and Command cannot both be set simultaneously")
        return value


class BackupSection(BaseModel):
    name: str
    schedule: Frequency
    sources: List[Source]


class GeneralSection(BaseModel):
    url: AnyUrl
    http_verb: HttpMethod
    requests_properties: Optional[Dict[str, str]]
    healthchecks_io_api_key: Optional[str]
    file_field_name: Optional[str] = "file"


class Config(BaseModel):
    general: GeneralSection
    backups: List[BackupSection]
