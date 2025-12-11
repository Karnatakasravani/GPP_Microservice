import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(file_path):
    """Load RSA private key from PEM file."""
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """Decrypt base64-encoded encrypted seed using RSA/OAEP with SHA-256."""
    
    # Remove whitespace and fix Base64 padding
    encrypted_seed_b64 = "".join(encrypted_seed_b64.split())
    missing_padding = len(encrypted_seed_b64) % 4
    if missing_padding:
        encrypted_seed_b64 += "=" * (4 - missing_padding)
    
    # Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    
    # RSA/OAEP decryption
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # The decrypted bytes ARE the UTF-8 encoded hex string
    # Decode to string first
    hex_seed = decrypted_bytes.decode('utf-8').strip()
    
    print(f"[DEBUG] Decrypted bytes length: {len(decrypted_bytes)}")
    print(f"[DEBUG] Hex seed (as string): {hex_seed}")
    print(f"[DEBUG] Hex seed length: {len(hex_seed)}")
    
    # Validate: must be 64-character hex string
    if len(hex_seed) != 64:
        raise ValueError(f"Seed length is {len(hex_seed)}, expected 64")
    
    if not all(c in "0123456789abcdef" for c in hex_seed.lower()):
        bad_chars = set(hex_seed.lower()) - set("0123456789abcdef")
        raise ValueError(f"Seed contains invalid hex characters: {bad_chars}")
    
    # Return lowercase hex
    return hex_seed.lower()

def main():
    print("\n" + "=" * 70)
    print("DECRYPTING SEED")
    print("=" * 70)
    
    private_key = load_private_key("keys/private.pem")

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()
    
    print(f"\n[1] Encrypted seed loaded")
    print(f"    Length: {len(encrypted_seed_b64)} chars")

    print(f"\n[2] Decrypting...")
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
    
    print(f"\n[3] SUCCESS!")
    print(f"    Decrypted seed (64-char hex): {hex_seed}")
    
    # Save to file
    with open("data/seed.txt", "w") as f:
        f.write(hex_seed)
    print(f"    Saved to seed.txt")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()