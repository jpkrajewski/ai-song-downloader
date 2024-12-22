import json
import logging
from typing import Dict, List, Optional

import requests
import yt_dlp
from bs4 import BeautifulSoup

from aisd.src.config import config
from aisd.src.helpers import Maybe

logger = logging.getLogger(__name__)

# Constants for script tag indices and JSON keys
SCRIPT_TAG_INDEX = 23
PATHS: Dict[str, list] = {
    "entries": [
        "contents",
        "twoColumnSearchResultsRenderer",
        "primaryContents",
        "sectionListRenderer",
        "contents",
        0,
        "itemSectionRenderer",
        "contents",
    ],
    "video_renderer_inlineplaybackendpoint_url": [
        "videoRenderer",
        "inlinePlaybackEndpoint",
        "commandMetadata",
        "webCommandMetadata",
        "url",
    ],
    "video_renderer_navigationendpoint_url": [
        "videoRenderer",
        "navigationEndpoint",
        "commandMetadata",
        "webCommandMetadata",
        "url",
    ],
    "metadata_rows": [
        "lockupViewModel",
        "metadata",
        "lockupMetadataViewModel",
        "metadata",
        "contentMetadataViewModel",
        "metadataRows",
    ],
    "fallback_url": [
        "metadataParts",
        0,
        "text",
        "commandRuns",
        0,
        "onTap",
        "innertubeCommand",
        "commandMetadata",
        "webCommandMetadata",
        "url",
    ],
}


def safe_get(
    dct: dict, keys: List[str], default=None, raises=False
) -> Optional[str | list | dict]:
    """Safely get a nested value in a dictionary with a list of keys."""
    traversed = []
    for key in keys:
        try:
            dct = dct[key]
            traversed.append(key)
        except (KeyError, TypeError, IndexError) as e:
            logger.warning(
                f"Key '{key}' is missing or invalid type. Traversed keys: {traversed}. Exception: {str(e)}"
            )
            if raises:
                raise e
            return default
    return dct


def get_yt_url(song_title: str) -> Optional[str]:
    """Get the first YouTube video URL for the given song title."""
    logger.info(f"Getting YouTube URL for: {song_title}")

    # Prepare search query URL
    query = song_title.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    logger.debug(f"Constructed search URL: {url}")

    return (
        Maybe(url)
        .bind(fetch_page)
        .bind(parse_html_to_json)
        .bind(extract_url_from_payload)
        .get_or_else(None)
    )


def fetch_page(url: str) -> Optional[requests.Response]:
    """Fetch the webpage using requests and return the response."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Request successful for: {url}")
        return response
    except requests.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None


def parse_html_to_json(response: requests.Response) -> Optional[dict]:
    """Parse HTML response to extract JSON data."""
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.select("script")[SCRIPT_TAG_INDEX].text
        logger.debug("Successfully extracted script tag for parsing.")
        data = script_tag.replace("var ytInitialData = ", "")[:-1]
        return json.loads(data)
    except Exception as e:
        logger.error(f"Failed to extract or parse script tag: {e}")
        return None


def extract_url_from_payload(data: dict) -> Optional[str]:
    """Extract YouTube URL from parsed JSON payload."""
    try:
        entries = safe_get(data, PATHS["entries"], raises=True)
        found_url = None

        # Search for videoRenderer inlinePlaybackEndpoint URL
        if isinstance(entries, list):
            for entry in entries:
                if "videoRenderer" in entry:
                    found_url = safe_get(
                        entry, PATHS["video_renderer_inlineplaybackendpoint_url"]
                    )
                    if not found_url:
                        found_url = safe_get(
                            entry, PATHS["video_renderer_navigationendpoint_url"]
                        )
                    if found_url:
                        break
            # If not found in videoRenderer, check metadata rows
            if not found_url:
                for entry in entries:
                    rows = safe_get(entry, PATHS["metadata_rows"], default=[])
                    if isinstance(rows, list):
                        for row in rows:
                            url = safe_get(row, PATHS["fallback_url"])
                            if url:
                                found_url = url
                                break
                        if found_url:
                            break

        if found_url and isinstance(found_url, str):
            result = found_url.split("&")[
                0
            ]  # Extract base URL without query parameters
            final_url = "https://www.youtube.com" + result
            logger.info(f"Successfully extracted YouTube URL: {final_url}")
            return final_url
        else:
            logger.warning("No valid URL found in the data.")
            return None

    except Exception as e:
        logger.error(f"Error extracting URL: {e}")
        return None


def download_youtube_as_mp3(youtube_urls: List[str], output_folder: str = "downloads"):
    """Download YouTube videos as MP3 using yt-dlp."""
    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ignoreerrors": True,
        "logger": logger,
        "min_views": config.YTDLP_MIN_VIEWS,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(youtube_urls)
        logger.info("Download complete.")
    except yt_dlp.DownloadError as e:
        logger.error(f"Failed to download videos: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during download: {e}")
