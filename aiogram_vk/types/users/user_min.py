from typing import Optional
from ..base import VkObject


class UserMin(VkObject):
    id: int
    "User ID"
    first_name: Optional[str] = None
    "User first name"
    last_name: Optional[str] = None
    "User last name"
    deactivated: Optional[str] = None
    "Returns if a profile is deleted or blocked"
    hidden: Optional[bool] = None
    "Returns if a profile is hidden."
    can_access_closed: Optional[bool] = None
    is_closed: Optional[bool] = None
