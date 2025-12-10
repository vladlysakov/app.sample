"""Sample application demonstrating Rick and Morty API client usage.

This script fetches all characters, locations, and episodes from the API
and saves them to separate JSON files.
"""

import asyncio
import json
from pathlib import Path
from typing import List

from client import Character, Episode, Location, RickMortyClient

OUTPUT_DIR = Path("data")


def save(output_path: str, entities):
    output_file = OUTPUT_DIR / output_path
    with output_file.open("w") as f:
        json.dump(
            [ep.model_dump(mode="json") for ep in entities],
            f,
            indent=2,
            ensure_ascii=False
        )


async def fetch_and_save_characters(client: RickMortyClient):
    characters: List[Character] = []

    async for character in client.get_all_characters():
        characters.append(character)

    save("characters.json", characters)


async def fetch_and_save_locations(client: RickMortyClient) -> None:
    locations: List[Location] = []

    async for location in client.get_all_locations():
        locations.append(location)

    save("locations.json", locations)


async def fetch_and_save_episodes(client: RickMortyClient) -> None:
    episodes: List[Episode] = []

    async for episode in client.get_all_episodes():
        episodes.append(episode)

    save("episodes.json", episodes)


async def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with RickMortyClient() as client:
        await asyncio.gather(
            fetch_and_save_characters(client),
            fetch_and_save_locations(client),
            fetch_and_save_episodes(client),
        )

    print(f"All data fetched and saved successfully to {OUTPUT_DIR.absolute()}!")


if __name__ == "__main__":
    asyncio.run(main())
