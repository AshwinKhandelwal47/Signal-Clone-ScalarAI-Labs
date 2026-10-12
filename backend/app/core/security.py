<<<<<<< HEAD
import hashlib
import secrets


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
=======
"""Cryptographic helpers for session tokens."""

import hashlib
import secrets


def generate_token() -> str:
    """Generates a high-entropy URL-safe bearer token string."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Calculates the SHA-256 hex digest of a bearer token for safe database persistence."""
    return hashlib.sha256(token.encode()).hexdigest()

>>>>>>> 653fe1e (commented code)
