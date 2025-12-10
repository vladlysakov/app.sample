"""Async HTTP client for Rick and Morty API."""

from typing import AsyncIterator, Type, TypeVar

import httpx
from pydantic import BaseModel

from .models import Character, Episode, Location
from .types import PaginatedResponse

T = TypeVar("T", bound=BaseModel)

BASE_URL = "https://rickandmortyapi.com/api"


class RickMortyClient:
    def __init__(self, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    class _Endpoints:
        character = "/character"
        episode = "/episode"
        location = "/location"

    class HTTPClientNotInitialized(Exception):
        default_msg = "Client not initialized. Use async context manager."

        def __init__(self, message=default_msg):
            self.message = message
            super().__init__(self.message)

    async def __aenter__(self) -> "RickMortyClient":
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout)
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client:
            await self._client.aclose()

    async def _fetch_page(
            self, endpoint: str, page: int, model: Type[T]
    ) -> PaginatedResponse[T]:
        if not self._client:
            raise self.HTTPClientNotInitialized()

        response = await self._client.get(endpoint, params={"page": page})
        response.raise_for_status()

        data = response.json()
        return PaginatedResponse[model](
            info=data["info"],
            results=[model.model_validate(item) for item in data["results"]]
        )

    async def _fetch_all(self, endpoint: str, model: Type[T]) -> AsyncIterator[T]:
        page = 1
        while True:
            paginated = await self._fetch_page(endpoint, page, model)

            for item in paginated.results:
                yield item

            if not paginated.info.next:
                break

            page += 1

    async def get_all_characters(self) -> AsyncIterator[Character]:
        async for character in self._fetch_all(self._Endpoints.character, Character):
            yield character

    async def get_all_locations(self) -> AsyncIterator[Location]:
        async for location in self._fetch_all(self._Endpoints.location, Location):
            yield location

    async def get_all_episodes(self) -> AsyncIterator[Episode]:
        async for episode in self._fetch_all(self._Endpoints.episode, Episode):
            yield episode

    async def get_character(self, character_id: int) -> Character:
        return await self.get_single_entity(self._Endpoints.character, character_id, Character)

    async def get_location(self, location_id: int) -> Location:
        return await self.get_single_entity(self._Endpoints.location, location_id, Location)

    async def get_episode(self, episode_id: int) -> Episode:
        return await self.get_single_entity(self._Endpoints.episode, episode_id, Episode)

    async def get_single_entity(self, path: str, entity_id: int, model: Type[T]) -> T:
        if not self._client:
            raise self.HTTPClientNotInitialized()

        response = await self._client.get(f"{path}/{entity_id}")
        response.raise_for_status()
        return model.model_validate(response.json())
