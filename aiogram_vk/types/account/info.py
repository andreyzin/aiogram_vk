from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import Field

from ..base import VkObject


class AccountInfo(VkObject):
    """
    This object represents a Vk user or bot.
    """

    two_fa_required: Optional[bool] = Field(None, alias="2fa_required")
    "Two factor authentication is enabled"
    https_required: Optional[bool] = None
    "Information whether HTTPS-only is enabled"
    intro: Optional[int] = None
    "Information whether user has been processed intro"
    lang: Optional[int] = None
    "Language ID"
    no_wall_replies: Optional[bool] = None
    "Information whether wall comments should be hidden"
    own_posts_default: Optional[bool] = None
    "Information whether only owners posts should be shown"
    country: Optional[str] = None
    "User country"
    community_comments: Optional[bool] = None
    "Information whether community comments should be shown"
    link_redirects: Optional[Dict[str, str]] = None
    "Link redirects"
    vk_pay_endpoint_v2: Optional[str] = None
    "VK Pay endpoint v2"
    vk_pay_app_id: Optional[int] = None
    "VK Pay app id"
    messages_translation_language_pairs: Optional[List[str]] = None
    "Messages translation language pairs"
    obscene_text_filter: Optional[bool] = None
    "Information whether obscene text filter is enabled"
    can_change_password: Optional[bool] = None
    "Information whether user can change password"
