# Auto-generated token loader - stores encrypted token
# Decrypts token at runtime using IP_HASH provided separately.
import binascii

_ip_hash = "751e8fdd1b55d3fbf6f4a8d8f7dda4f4"

def _xor_decrypt(hex_cipher: str, key: str) -> str:
    cipher = binascii.unhexlify(hex_cipher)
    keyb = key.encode('utf-8')
    plain_bytes = bytes([b ^ keyb[i % len(keyb)] for i, b in enumerate(cipher)])
    return plain_bytes.decode('utf-8')

_encrypted_token_hex = "0f0703550f56545d07500f74257b320c537d2402295f534a2b6e25222b5d2c4075725b2e542a005c42076d743d54"

def get_token() -> str:
    """
    Returns the decrypted token. This function decrypts the token in-memory
    using the IP_HASH. Do not print the token in logs.
    """
    return _xor_decrypt(_encrypted_token_hex, _ip_hash)

# Also expose IP_ID and IP_HASH if needed
IP_ID = "7722416548"
IP_HASH = "751e8fdd1b55d3fbf6f4a8d8f7dda4f4"