from typing import Any, List, Optional

from ..audio.audio import Audio
from ..base import VkObject
from .user_min import UserMin


class UserSettingsXtr(VkObject):
    connections: Optional[Any] = None  # users_user_connections
    bdate: Optional[str] = None
    "User's date of birth"
    bdate_visibility: Optional[int] = None
    "Information whether user's birthdate are hidden"
    city: Optional[Any] = None  # base_city
    first_name: Optional[str] = None
    "User first name"
    home_town: str
    "User's hometown"
    last_name: Optional[str] = None
    "User last name"
    maiden_name: Optional[str] = None
    "User maiden name"
    name_request: Optional[Any] = None  # account_name_request
    personal: Optional[Any] = None  # users_personal
    phone: Optional[str] = None
    "User phone number with some hidden digits"
    relation: Optional[Any] = None  # users_user_relation
    "User relationship status"
    relation_partner: Optional[UserMin] = None
    relation_pending: Optional[bool] = None
    "Information whether relation status is pending"
    relation_requests: Optional[List[UserMin]] = None
    screen_name: Optional[str] = None
    "Domain name of the user's page"
    sex: Optional[int] = None
    "User sex"
    status: str
    "User status"
    status_audio: Optional[Audio] = None
    interests: Optional[Any] = None  # account_user_settings_interests
    languages: Optional[List[str]] = None
