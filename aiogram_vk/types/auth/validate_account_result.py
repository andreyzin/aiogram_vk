from __future__ import annotations

from typing import List

from ..base import VkObject


class AuthValidateAccountResult(VkObject):
    """
    ValidateAccount
    """

    is_phone: bool
    flow_name: str
    flow_names: List[str]
    sid: str