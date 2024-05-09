from typing import Optional

from pydantic import AnyUrl

from aiogram_vk.types.base import VkObject
from aiogram_vk.types.custom import DateTime


class Audio(VkObject):
    access_key: Optional[str] = None
    "Access key for the audio"
    artist: str
    "Artist name"
    id: int
    "Audio ID"
    owner_id: int
    "Audio owner's ID"
    title: str
    "Title"
    url: Optional[AnyUrl] = None
    "URL of mp3 file"
    duration: int
    "Duration in seconds"
    stream_duration: Optional[int] = None
    "Stream duration in seconds"
    date: Optional[DateTime] = None
    "Date when uploaded"
    album_id: Optional[int] = None
    "Album ID"
    performer: Optional[str] = None
    "Date when uploaded"
    is_explicit: Optional[bool] = None
    "Whether the audio is explicit"
    is_focus_track: Optional[bool] = None
    "Whether the audio is a focus track"
    is_licensed: Optional[bool] = None
    "Whether the audio is licensed"
    track_code: Optional[str] = None
    "Track code"
    genre_id: Optional[int] = None
    "Genre ID"
    no_search: Optional[bool] = None
    short_videos_allowed: Optional[bool] = None
    "Whether short videos are allowed"
    stories_allowed: Optional[bool] = None
    "Whether stories are allowed"
    stories_cover_allowed: Optional[bool] = None
    "Whether stories cover are allowed"
    release_audio_id: Optional[str] = None
