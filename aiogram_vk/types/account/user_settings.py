from typing import Optional

from pydantic import AnyUrl

from ..users.user_settings_xtr import UserSettingsXtr
from ..users.user_min import UserMin


class AccountUserSettings(UserMin, UserSettingsXtr):
    photo_200: Optional[AnyUrl]
    is_service_account: Optional[bool]
