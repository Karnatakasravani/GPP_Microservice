import base64
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    hex_seed = hex_seed.strip()
    raw = bytes.fromhex(hex_seed)
    return base64.b32encode(raw).decode("ascii")

def generate_totp_code(hex_seed: str) -> str:
    secret_b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(secret_b32, digits=6, interval=30)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    secret_b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(secret_b32, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)