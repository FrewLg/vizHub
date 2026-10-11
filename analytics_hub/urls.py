"""
Page URL patterns for analytics_hub.
Included inside i18n_patterns so every route gets a /en/… or /am/… prefix.
"""
from django.urls import path
from . import views
from .views import ObservationBarChartView

urlpatterns = [
    path("",           ObservationBarChartView.as_view(), name="dashboard"),
    path("upload/",    views.upload_view,                 name="upload_data"),
    path("export-pdf/", views.download_pdf_report,        name="export_pdf"),
    path("viz/bar/old", views.dashboard_view,             name="observation-bar-chart"),
]
