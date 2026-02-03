class VkError(Exception):
    pass


class AuthError(VkError):
    pass


class CaptchaError(AuthError):
    pass


class Need2FAError(AuthError):
    pass


class InvalidClient(AuthError):
    pass

class IncorrectPassword(AuthError):
    pass