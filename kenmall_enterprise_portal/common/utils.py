"""Enterprise portal common utils file."""
from kenmall_enterprise_portal.edi_client.client import EDIClient
from django.conf import settings
from kenmall_enterprise_portal.config import settings

def get_edi_client():
    client = EDIClient(
        config={
        "host": settings.EDI_BASE_URL,
        "scheme": settings.EDI_SCHEME,
        "api_url": settings.EDI_API_URL,
        "oauth_id": '',
        "oauth_secret": '',
        "user_email": '',
        "user_password": '',
        "token_url": None,
        "timeout_retries": 6,
        "timeout_retry_delay": 10,
        "auth_retries": 3,
        "auth_retry_delay": 1,
    })
    return client
