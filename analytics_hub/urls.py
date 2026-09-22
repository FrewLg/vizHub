from django.urls import path
from . import views
from django.db.models import Sum, Avg, Count, Max
from .views import ObservationBarChartView

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload_data'),
    path('export-pdf/', views.download_pdf_report, name='export_pdf'), 
        path('api/chatbot/', views.ai_chatbot_api, name='ai_chatbot_api'),
path(
        "viz/bar/",
        ObservationBarChartView.as_view(),
        name="observation-bar-chart",
    ),
    path("api/analysis/<slug:slug>/", views.analysis_data     ), 
]

 