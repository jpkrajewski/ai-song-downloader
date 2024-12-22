import logging

import typer

from aisd.src.ai import get_provider
from aisd.src.download import download_youtube_as_mp3, get_yt_url

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def from_prompt(prompt: str):
    """Get the titles of the songs for a given prompt using AI."""
    logger.info(f"Getting songs for prompt: {prompt}")
    songs = list(set(get_provider().get_songs_from_prompt(prompt)))
    logger.info(f"Got song names: {songs}")
    song_urls = (get_yt_url(song) for song in songs)
    download_youtube_as_mp3([url for url in song_urls if url is not None])


@app.command()
def from_playlist(url: str):
    """Get songs from playlist"""
    download_youtube_as_mp3([url])


if __name__ == "__main__":
    app()
