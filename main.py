from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from decrypted_seed import decrypt_seed, load_private_key
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()
DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

SEED_FILE = DATA_DIR / "seed.txt"

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyCodeRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: DecryptSeedRequest):
    try:
        private_key = load_private_key("keys/private.pem")
        hex_seed = decrypt_seed(body.encrypted_seed, private_key)
        SEED_FILE.write_text(hex_seed)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    hex_seed = SEED_FILE.read_text().strip()
    code = generate_totp_code(hex_seed)

    import time
    now = int(time.time())
    valid_for = 30 - (now % 30)

    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa(body: VerifyCodeRequest):
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    if not body.code:
        raise HTTPException(status_code=400, detail="Missing code")

    hex_seed = SEED_FILE.read_text().strip()
    is_valid = verify_totp_code(hex_seed, body.code, valid_window=1)
    return {"valid": is_valid}