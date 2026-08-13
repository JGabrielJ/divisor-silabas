#! divisor_app/services/core_api.py

import hashlib
import hmac

import requests
from django.conf import settings

from .exceptions import CoreAPIError


class CoreAPIClient:
    def __init__(
        self, api_key: str | None = None, extra_headers: dict[str, str] | None = None
    ) -> None:
        self.headers: dict[str, str] = {}

        if api_key:
            self.headers["X-API-Key"] = api_key

        if settings.API_SITE_TOKEN:
            self.headers["X-Site-Token"] = settings.API_SITE_TOKEN
            self.headers["X-Site-Signature"] = _build_site_signature(
                settings.API_SITE_TOKEN
            )

        if extra_headers:
            self.headers.update(extra_headers)

    def analyze_word(self, word: str) -> dict:
        response = requests.post(
            f"{settings.API_BASE_URL}/v1/analyze",
            json={"word": word},
            headers=self.headers,
            timeout=5,
        )

        if response.ok:
            return response.json()

        message = response.text

        try:
            payload = response.json()
            if isinstance(payload, dict) and "detail" in payload:
                message = str(payload["detail"])

        except ValueError:
            pass

        raise CoreAPIError(response.status_code, message)


def _build_site_signature(token: str) -> str:
    return hmac.new(
        token.encode(),
        b"divisorsilabas-site",
        hashlib.sha256,
    ).hexdigest()
