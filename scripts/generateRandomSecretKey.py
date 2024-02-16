import secrets


def generate_secret_key(length: int = 32) -> str:
    """
    Generates a random secret key.

    Args:
        length (int): The length of the secret key in bytes. Default is 32 bytes.

    Returns:
        str: The generated random secret key.
    """
    return secrets.token_hex(length)


# Generate a secret key of default length (32 bytes)
secret_key = generate_secret_key()
print("Generated Secret Key:", secret_key)
