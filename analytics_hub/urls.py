from django.urls import path
from . import views
from .views import ObservationBarChartView

urlpatterns = [
    path('viz/bar/old', views.dashboard_view, name='observation-bar-chart'),
    path('upload/', views.upload_view, name='upload_data'),
    path('export-pdf/', views.download_pdf_report, name='export_pdf'), 
    path('api/chatbot/', views.ai_chatbot_api, name='ai_chatbot_api'),
    path(
        "",
        ObservationBarChartView.as_view(),
        name="dashboard",
    ),
    path("api/analysis/<slug:slug>/", views.analysis_data ), 
]