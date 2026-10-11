import os


def google_client_id(request):
    """Expose GOOGLE_CLIENT_ID to every template for Google One Tap."""
    return {
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID", ""),
    }
