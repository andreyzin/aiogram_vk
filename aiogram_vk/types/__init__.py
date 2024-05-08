from typing import List, Literal, Optional, Union

from .account_info import AccountInfo
from .audio_search_result import AudioSearchResult
from .base import UNSET_PARSE_MODE, VkObject
from .custom import DateTime
from .error import Error
from .input_file import InputFile

__all__ = (
    "Error",
    "DateTime",
    "VkObject",
    "UNSET_PARSE_MODE",
    "InputFile",
    "AccountInfo",
    "AudioSearchResult",
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
