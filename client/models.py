"""Domain models for Rick and Morty API entities."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl


class Character(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: dict[str, str]
    location: dict[str, str]
    image: HttpUrl
    episode: List[str]
    url: str
    created: datetime


class Location(BaseModel):
    id: int
    name: str
    type: str
    dimension: str
    residents: List[str]
    url: str
    created: datetime


class Episode(BaseModel):
    id: int
    name: str
    air_date: str
    episode: str
    characters: List[str]
    url: str
    created: datetime
