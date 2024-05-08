from enum import Enum


class AccountFields(str, Enum):
    """Account fields"""

    country = "country"
    https_required = "https_required"
    own_posts_default = "own_posts_default"
    no_wall_replies = "no_wall_replies"
    intro = "intro"
    lang = "lang"
