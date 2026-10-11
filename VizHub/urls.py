from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.http import HttpResponseRedirect


def redirect_to_default_language(request):
    """Redirect bare / to /en/ (or whatever LANGUAGE_CODE is set to)."""
    lang = settings.LANGUAGE_CODE  # 'en'
    # Preserve any query string (filter params)
    qs = ("?" + request.META.get("QUERY_STRING", "")) if request.META.get("QUERY_STRING") else ""
    return HttpResponseRedirect(f"/{lang}/{qs}")


# ── Prefix-free routes ─────────────────────────────────────────────────────────
# Admin, auth, i18n switcher, and all /api/… endpoints live here so they are
# never broken by a language prefix and AJAX fetch calls always resolve.
urlpatterns = [
    path("",          redirect_to_default_language),          # / → /en/
    path("admin/",    admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("i18n/",     include("django.conf.urls.i18n")),      # set_language view
    path("api/",      include("analytics_hub.urls_api")),     # AJAX endpoints
]

# ── Language-prefixed page routes  →  /en/  /am/  /fr/ ───────────────────────
urlpatterns += i18n_patterns(
    path("", include("analytics_hub.urls")),
    prefix_default_language=True,   # /en/ is always explicit
)
