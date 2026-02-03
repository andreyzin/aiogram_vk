from typing import List, Literal, Optional, Union

from .account.info import AccountInfo
from .account.user_settings import AccountUserSettings
from .audio.audio import Audio
from .audio.search_result import AudioSearchResult
from .auth.get_oauth_token_result import GetOauthTokenResult
from .auth.validate_account_result import AuthValidateAccountResult
from .base import UNSET_PARSE_MODE, VkObject
from .captcha import Captcha, CaptchaAnswer
from .custom import DateTime
from .error import Error
from .input_file import InputFile
from .users.user_min import UserMin
from .users.user_settings_xtr import UserSettingsXtr

__all__ = (
    "AccountInfo",
    "AccountUserSettings",
    "Audio",
    "AudioSearchResult",
    "GetOauthTokenResult",
    "AuthValidateAccountResult",
    "VkObject",
    "UNSET_PARSE_MODE",
    "Captcha",
    "CaptchaAnswer",
    "DateTime",
    "Error",
    "InputFile",
    "UserMin",
    "UserSettingsXtr",
)

# Load typing forward refs for every VkObject
for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "model_rebuild"):
        continue
    _entity.model_rebuild(
        _types_namespace={
            "List": List,
            "Optional": Optional,
            "Union": Union,
            "Literal": Literal,
            **{k: v for k, v in globals().items() if k in __all__},
        }
    )

del _entity
del _entity_name
