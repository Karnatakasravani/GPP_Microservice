import base64
import pyotp

# 1️⃣ Read hex seed in binary and decode safely
with open("decrypted_seed.txt", "r", encoding="utf-8") as f:
    hex_seed = f.read().strip()

# 2️⃣ Convert hex to bytes
seed_bytes = bytes.fromhex(hex_seed)

# 3️⃣ Convert bytes to base32 string (needed for TOTP)
seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')

# 4️⃣ Create TOTP object
totp = pyotp.TOTP(seed_base32, digits=6, interval=30)

# 5️⃣ Generate current TOTP code
totp_code = totp.now()

print("Current TOTP code:", totp_code)