import hashlib

def calculate_hash(data: str) -> str:
    """Calculates SHA256 hash of a string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def sign_data(data: str) -> (str, str):
    """Simulates a signer creating a message and its hash (signature)."""
    original_hash = calculate_hash(data)
    print(f"--- Signer's Side ---")
    print(f"Original Message: '{data}'")
    print(f"Calculated Hash (Signature): {original_hash}")
    print(f"Message and hash are prepared for sending.")
    return data, original_hash

def verify_data(received_data: str, received_hash: str, simulate_tampering: bool = False):
    """Simulates a verifier checking the message integrity against a received hash."""
    print(f"\n--- Verifier's Side ---")
    print(f"Received Message: '{received_data}'")
    print(f"Received Hash (Signature): {received_hash}")

    data_to_verify = received_data
    if simulate_tampering:
        # This simulates a subtle, unintentional change to the data *after* signing
        # but *before* the verifier re-hashes it. This is the core "mysterious failure" scenario
        # where the verifier is 'honest' but the data itself has been altered.
        data_to_verify = received_data.replace("world", "worLd", 1) # Change 'l' to 'L'
        print(f"!!! ALERT: Data subtly altered during transit/processing for demonstration.")
        print(f"Data used for re-hashing: '{data_to_verify}'")

    # The verifier honestly re-calculates the hash of the data they received (or processed).
    recalculated_hash = calculate_hash(data_to_verify)
    print(f"Verifier's Recalculated Hash: {recalculated_hash}")

    if recalculated_hash == received_hash:
        print(f"Verification SUCCESS: The data's integrity is confirmed.")
    else:
        # This demonstrates the article's concept: failure despite 'honest' parties.
        print(f"Verification FAILED: The recalculated hash does NOT match the received hash.")
        print(f"This indicates the data was altered after it was signed, even if unintentionally.")

# --- Main Execution ---
if __name__ == "__main__":
    original_message = "Hello, world! This is a secret message."

    # Scenario 1: Successful verification (no tampering)
    print("--- Scenario 1: Successful Verification ---")
    signed_message, signature = sign_data(original_message)
    verify_data(signed_message, signature, simulate_tampering=False)

    print("\n" + "="*70 + "\n")

    # Scenario 2: Failed verification due to subtle tampering (mysterious failure)
    print("--- Scenario 2: Failed Verification (Mysterious Failure) ---")
    # The signer still sends the original message and its correct hash.
    signed_message_tampered, signature_tampered = sign_data(original_message)
    # The 'simulate_tampering=True' flag here represents an external, unintentional change
    # to the data *before* the verifier performs their integrity check.
    verify_data(signed_message_tampered, signature_tampered, simulate_tampering=True)
