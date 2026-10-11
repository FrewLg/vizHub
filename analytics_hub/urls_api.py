"""
API-only URL patterns for analytics_hub.
These are included WITHOUT a language prefix so AJAX calls always resolve.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("chart-data/",             views.chart_data_api,  name="chart_data_api"),
    path("geojson/",                views.geojson_api,     name="geojson_api"),
    path("chatbot/",                views.ai_chatbot_api,  name="ai_chatbot_api"),
    path("analysis/<slug:slug>/",   views.analysis_data,   name="analysis_data"),
]
