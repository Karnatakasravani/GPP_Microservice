import pyotp
import base64

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    
    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: Number of periods before/after to accept (default 1 = ±30s)
    
    Returns:
        True if code is valid, False otherwise
    """
    try:
        # 1. Convert hex seed to bytes
        seed_bytes = bytes.fromhex(hex_seed)
        
        # 2. Convert bytes to base32
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        
        # 3. Create TOTP object
        totp = pyotp.TOTP(base32_seed)
        
        # 4. Verify code with time window tolerance
        # valid_window allows ±valid_window periods (each period is 30 seconds)
        return totp.verify(code, valid_window=valid_window)
    
    except Exception as e:
        print("Error verifying TOTP:", e)
        return False


# Example usage:
if __name__ == "__main__":
    hex_seed = "9075c1d9ff03c45211bb7edbad48e6d867472fa15a6d6442f612a6522b3b5860"
    code = "142616"  # Replace with code you want to verify
    result = verify_totp_code(hex_seed, code)
    print("Is code valid?", result)
