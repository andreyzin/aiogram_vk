import hashlib


def calculate_hash(input_str: str, nonce: int) -> str:
    """
    Считает SHA-256 от input_str + nonce и возвращает hex-строку.
    """
    data = f"{input_str}{nonce}".encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def perform_pow(input_str: str, difficulty: int):
    """
    Подбирает nonce так, чтобы хэш начинался с difficulty нулей.
    Возвращает (nonce, hash).
    """
    prefix = "0" * difficulty
    nonce = 0
    while True:
        hash_hex = calculate_hash(input_str, nonce)
        if hash_hex.startswith(prefix):
            return hash_hex
        nonce += 1


# Пример использования
if __name__ == "__main__":
    pow_input = "z1ACiy50UFd6cz9g"
    difficulty = 2
    hash_result = perform_pow(pow_input, difficulty)
    print(f"✅ Решение найдено!\nHash: {hash_result}")
