from enum import Enum


class UserTokenScope(str, Enum):
    notify = "notify"
    "The user allowed to send him notifications (for flash/iframe applications)"
    friends = "friends"
    "Access to friends."
    photos = "photos"
    "Access to photos."
    audio = "audio"
    "Access to audio recordings."
    video = "video"
    "Access to video."
    stories = "stories"
    "Access to stories"
    pages = "pages"
    "Access to wiki pages"
    menu = "menu"
    "Add a link to the application in the menu on the left."
    wallmenu = "wallmenu"
    "Posts on the user's wall."
    status = "status"
    "Access to user status."
    notes = "notes"
    "Access to user notes."
    messages = "messages"
    "Access to advanced methods of working with messages (only for Standalone applications, past moderation )."
    wall = "wall"
    """Access to conventional and advanced methods of working with the wall. This right of access by default is not available for sites (ignored when trying to authorize for applications with the type "Website" or according to the scheme Authorization Code Flow )."""
    ads = "ads"
    "Access to advanced methods of working with the advertising API . Available for authorization according to the scheme Implicit Flow or Authorization Code Flow ."
    offline_5 = "offline<5"
    offline_14 = "offline<14"
    offline_21 = "offline<21"
    offline_25 = "offline<25"
    offline_29 = "offline<29"
    offline = "offline"
    "Access to API at any time (when using this option, the parameter expires_in returned with access_token contains 0 — an infinite token). It is not used in Open API."
    docs = "docs"
    "Access to documents."
    groups = "groups"
    "Access to user groups."
    notifications = "notifications"
    "Access to user response alerts."
    stats = "stats"
    "Access to statistics of groups and applications of the user, the administrator of which he is."
    email = "email"
    "Access to the user's email."
    adsweb = "adsweb"
    "Access to advertising API."
    leads = "leads"
    "Access to leads."
    exchange = "exchange"
    "Access to exchange ADS."
    market = "market"
    "Access to goods."
    phone = "phone"
    "Access to phone number."


user_token_scope_bits = {
    UserTokenScope.notify: 1 << 0,
    UserTokenScope.friends: 1 << 1,
    UserTokenScope.photos: 1 << 2,
    UserTokenScope.audio: 1 << 3,
    UserTokenScope.video: 1 << 4,
    UserTokenScope.offline_5: 1 << 5,
    UserTokenScope.stories: 1 << 6,
    UserTokenScope.pages: 1 << 7,
    UserTokenScope.menu: 1 << 8,
    UserTokenScope.wallmenu: 1 << 9,
    UserTokenScope.status: 1 << 10,
    UserTokenScope.notes: 1 << 11,
    UserTokenScope.messages: 1 << 12,
    UserTokenScope.wall: 1 << 13,
    UserTokenScope.offline_14: 1 << 14,
    UserTokenScope.ads: 1 << 15,
    UserTokenScope.offline: 1 << 16,
    UserTokenScope.docs: 1 << 17,
    UserTokenScope.groups: 1 << 18,
    UserTokenScope.notifications: 1 << 19,
    UserTokenScope.stats: 1 << 20,
    UserTokenScope.offline_21: 1 << 21,
    UserTokenScope.email: 1 << 22,
    UserTokenScope.adsweb: 1 << 23,
    UserTokenScope.leads: 1 << 24,
    UserTokenScope.offline_25: 1 << 25,
    UserTokenScope.exchange: 1 << 26,
    UserTokenScope.market: 1 << 27,
    UserTokenScope.phone: 1 << 28,
    UserTokenScope.offline_29: 1 << 29,
}


def calculate_user_token_scope_value(scopes: list[UserTokenScope]):
    """
    Calculates a numeric value for a set of UserTokenScope.
    """
    value = 0
    for scope in scopes:
        bit = user_token_scope_bits.get(scope)
        if bit is not None:
            value |= bit
    return value


def scopes_from_value(value: int, remove_duplicate: bool = True):
    """
    Gets a set of UserTokenScope from a numeric value.
    """
    selected_scopes: set[UserTokenScope] = set()
    ost = value
    for scope, bit in user_token_scope_bits.items():
        if value & bit:  # проверяем, установлен ли бит
            if "<" in scope.value and remove_duplicate:
                scope = UserTokenScope(scope.value.split("<", 1)[0])
            selected_scopes.add(scope)

    return selected_scopes
