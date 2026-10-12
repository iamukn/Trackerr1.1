
import hashlib, hmac
import secrets

from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from affiliate.models import AffiliateSession


SESSION_DURATION = timedelta(days=7)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_affiliate_session(affiliate):
    # 32 cryptographically random bytes, URL-safe encoded.
    raw_token = secrets.token_urlsafe(32)

    session = AffiliateSession.objects.create(
        affiliate=affiliate,
        token_hash=hash_token(raw_token),
        expires_at=timezone.now() + SESSION_DURATION,
    )

    # Return the raw token once. Never store it in plaintext.
    return raw_token


def generate_otp():
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(email, otp):
    message = f"{email.strip().lower()}:{otp}".encode("utf-8")

    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        message,
        hashlib.sha256,
    ).hexdigest()


def verify_otp_hash(email, otp, stored_hash):
    return hmac.compare_digest(
        hash_otp(email, otp),
        stored_hash,
    )
