from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload_data'),
    path('export-pdf/', views.download_pdf_report, name='export_pdf'),  # <--- Added route
    path('api/chatbot/', views.ai_chatbot_api, name='ai_chatbot_api'),
]
