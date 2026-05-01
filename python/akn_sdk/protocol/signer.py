# akn/sdk/python/akn_sdk/protocol/signer.py

# import json

# def canonicalize(payload: dict):
#     return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


# akn/sdk/python/akn_sdk/protocol/signer.py

import json
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder


def canonicalize(payload: dict) -> bytes:
    """
    Deterministic JSON serialization for signing.
    """
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


def generate_keypair() -> dict:
    """
    Generate Ed25519 keypair.
    Returns base64 encoded keys.
    """
    signing_key = SigningKey.generate()

    private_key = signing_key.encode(
        encoder=Base64Encoder
    ).decode()

    public_key = signing_key.verify_key.encode(
        encoder=Base64Encoder
    ).decode()

    return {
        "private_key": private_key,
        "public_key": public_key,
    }


def sign_message(private_key: str, payload: dict) -> str:
    """
    Sign canonicalized payload.
    Returns base64 encoded signature.
    """
    signing_key = SigningKey(
        private_key.encode(),
        encoder=Base64Encoder
    )

    canonical = canonicalize(payload)

    signed = signing_key.sign(canonical)

    return Base64Encoder.encode(signed.signature).decode()