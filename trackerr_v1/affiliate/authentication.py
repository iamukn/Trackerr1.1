
from django.utils import timezone
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import AuthenticationFailed

from .models import AffiliateSession
from .security import hash_token


class AffiliateTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if auth[0].lower() != b"bearer":
            return None

        if len(auth) != 2:
            raise AuthenticationFailed("Invalid authorization header.")

        try:
            raw_token = auth[1].decode("utf-8")
        except UnicodeDecodeError:
            raise AuthenticationFailed("Invalid session token.")

        if not raw_token:
            raise AuthenticationFailed("Invalid session token.")

        session = (
            AffiliateSession.objects
            .select_related("affiliate")
            .filter(token_hash=hash_token(raw_token))
            .first()
        )

        if session is None:
            raise AuthenticationFailed("Invalid session.")

        now = timezone.now()

        if session.revoked_at is not None:
            raise AuthenticationFailed("Session revoked.")

        if session.expires_at <= now:
            raise AuthenticationFailed("Session expired.")

        if not session.affiliate.is_active:
            raise AuthenticationFailed("Affiliate account disabled.")

        return (session.affiliate, session)

    def authenticate_header(self, request):
        return "Bearer"
