from django.urls import path
from . import views
from django.db.models import Sum, Avg, Count, Max

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload_data'),
    path('export-pdf/', views.download_pdf_report, name='export_pdf'), 
        path('api/chatbot/', views.ai_chatbot_api, name='ai_chatbot_api'),

    path("api/analysis/<slug:slug>/", views.analysis_data     ), 
]
from django.db.models import Sum

def build_chart_data(queryset, viz_config):
    # Fallback chart type and x-axis field
    chart_type = viz_config.chart_type if (viz_config and viz_config.chart_type) else "line"
    x_axis_field = viz_config.x_axis if (viz_config and viz_config.x_axis) else "year"

    # Strict field mapping matching your exact model foreign keys & attributes
    field_mapping = {
        "year": "year",
        "location": "location__name",      # Matches Location.name
        "sex": "sex__name",                  # Matches Sex.name
        "cause": "cause__name",              # Matches Cause.name
        "age_group": "age_group__name",      # Matches AgeGroup.name
        "facility_category": "facility_category__name", # Matches FacilityCategory.name
        "date": "date",
    }

    group_field = field_mapping.get(x_axis_field, "year")

    # Perform aggregation on the filtered queryset
    aggregated_data = (
        queryset.values(group_field)
        .annotate(metric_sum=Sum("value"))
        .order_by(group_field)
    )

    labels = []
    values = []

    for entry in aggregated_data:
        label = entry[group_field]
        labels.append(str(label) if label is not None else "Unknown")
        values.append(float(entry["metric_sum"]) if entry["metric_sum"] is not None else 0.0)

    return {
        "type": chart_type,
        "labels": labels,
        "datasets": [
            {
                "label": viz_config.indicator.name if (viz_config and viz_config.indicator) else "Value",
                "data": values,
            }
        ],
    }