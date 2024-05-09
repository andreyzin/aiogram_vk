from typing import Any, Optional

from pydantic import AnyUrl

from .user_min import UserMin


class User(UserMin):
    sex: Optional[int] = None
    "User sex"
    screen_name: Optional[str] = None
    "Domain name of the user's page"
    photo_50: Optional[AnyUrl] = None
    "URL of square photo of the user with 50 pixels in width"
    photo_100: Optional[AnyUrl] = None
    "URL of square photo of the user with 100 pixels in width"
    online_info: Optional[Any] = None  # users_online_info
    online: Optional[bool] = None
    "Information whether the user is online"
    online_mobile: Optional[bool] = None
    "Information whether the user is online in mobile site or application"
    online_app: Optional[int] = None
    "Application ID"
    verified: Optional[bool] = None
    "Information whether the user is verified"
    trending: Optional[int] = None
    'Information whether the user has a "fire" pictogram.'
    friend_status: Optional[Any] = None  # friends_friend_status_status
    mutual: Optional[Any] = None  # friends_requests_mutual
