import secrets
import string


def generate_device_id(n: int = 21) -> str:
    """Generates a random string of length n from a given set of characters."""
    charset = f"{string.digits}{string.ascii_letters}-_"
    return "".join(secrets.choice(charset) for _ in range(n))
