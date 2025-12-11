import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API.
    """

    # 1. Read your public key (keep PEM markers)
    with open("keys/public.pem", "r") as f:
         public_key = f.read().strip()

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    print("\nSending request to Instructor API...\n")

    # 3. Send POST request
    try:
        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        # 4. Parse response
        if data.get("status") == "success":
            encrypted_seed = data.get("encrypted_seed")

            with open("encrypted_seed.txt", "w") as f:
                f.write(encrypted_seed)

            print("✅ Encrypted seed received!")
            print("📌 Saved to encrypted_seed.txt (DO NOT COMMIT THIS FILE)\n")
            return encrypted_seed

        else:
            print("❌ API returned error:", data)
            return None

    except Exception as e:
        print("❌ Request failed:", e)
        return None


# Run function with YOUR details
request_seed(
    student_id="22A91A4460",
    github_repo_url="https://github.com/Karnatakasravani/GPP_Microservice",
    api_url="https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
)
