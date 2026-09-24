import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import process_excel_upload
from django.http import HttpResponse
from .utils_pdf import generate_gbd_pdf_report
from django.utils.translation import get_language
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.chart_builder import build_chart_data 
from django.contrib import messages
from django.db.models import Avg, Sum, Count, Max
from .forms import ExcelUploadForm  
from django.views.generic import TemplateView
from .models import (
    Topic,
    Indicator,
    Location,
    Observation,
    Cause,
    Sex,
    VisualizationConfig,
    AgeGroup,
    FacilityCategory, )


# class ObservationBarChartView(TemplateView):
#     template_name = "analytics_hub/charts/bar_chart.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         indicator_name = "-"
#         geography = self.request.GET.get("geography", "regional")
#         topic_id = self.request.GET.get("topic")
#         indicator_id = self.request.GET.get("indicator")
#         year = self.request.GET.get("year")
#         location_id = self.request.GET.get("location")
#         cause_id = self.request.GET.get("cause")
#         sex_id = self.request.GET.get("sex")
#         if indicator_id:
#             try:
#                 indicator = Indicator.objects.get(pk=indicator_id)
#                 indicator_name = indicator.name
#             except Indicator.DoesNotExist:
#                 pass

#         context["indicator_name"] = indicator_name
#         queryset = Observation.objects.select_related("location", "indicator")
#         if geography == "national":
#             queryset = queryset.filter(location__level__iexact="country")
#         elif geography == "regional":
#             queryset = queryset.filter(location__level__in=["regional", "region", "Regional"])
#         elif geography == "zone":
#             queryset = queryset.filter(location__level__iexact="zone")
#         elif geography == "woreda":
#             queryset = queryset.filter(location__level__iexact="woreda")

#         # 4. Apply Faceted Search Filters
#         if topic_id:
#             queryset = queryset.filter(indicator__topic_id=topic_id)

#         if indicator_id:
#             queryset = queryset.filter(indicator_id=indicator_id)

#         if year:
#             queryset = queryset.filter(year=year)

#         if location_id:
#             queryset = queryset.filter(location_id=location_id)

#         if cause_id:
#             queryset = queryset.filter(cause_id=cause_id)

#         if sex_id:
#             queryset = queryset.filter(sex_id=sex_id)
#         data = (
#             queryset
#             .values("location__name")
#             .annotate(total=Sum("value"))
#             .order_by("-total")
#         )

#         labels = [row["location__name"] for row in data if row["location__name"]]
#         values = [float(row["total"]) if row["total"] is not None else 0.0 for row in data if row["location__name"]]

#         context["chart_labels"] = labels
#         context["chart_values"] = values

#         context["data"] = [
#             {
#                 "label": row["location__name"],
#                 "value": float(row["total"]) if row["total"] is not None else 0.0
#             }
#             for row in data if row["location__name"]
#         ]

#         context["show_map"] = True
#         context["topics"] = Topic.objects.all() if 'Topic' in globals() else []
#         context["indicators"] = Indicator.objects.all()
#         context["years"] = Observation.objects.values_list('year', flat=True).distinct().order_by('-year')
#         context["locations"] = Location.objects.all()
#         context["causes"] = Cause.objects.all() if 'Cause' in globals() else []
#         context["sexes"] = Sex.objects.all() if 'Sex' in globals() else []
#         context["selected_geography"] = geography
#         context["selected_topic"] = topic_id
#         context["selected_indicator"] = indicator_id
#         context["selected_year"] = year
#         context["selected_location"] = location_id
#         context["selected_cause"] = cause_id
#         context["selected_sex"] = sex_id
#         line_data = (
#             queryset
#             .values("year")
#             .annotate(total=Sum("value"))
#             .order_by("year")
#         )

#         context["line_chart_labels"] = [
#             str(row["year"]) for row in line_data
#         ]

#         context["line_chart_values"] = [
#             float(row["total"] or 0) for row in line_data
#         ]
#         return context

class ObservationBarChartView(TemplateView):
    # template_name = "analytics_hub/charts/barchart.html"
    template_name = "analytics_hub/charts/bar_chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indicator_name = "-"
        
        geography = self.request.GET.get("geography", "regional")
        topic_id = self.request.GET.get("topic")
        indicator_id = self.request.GET.get("indicator")
        year = self.request.GET.get("year")
        location_id = self.request.GET.get("location")
        cause_id = self.request.GET.get("cause")
        sex_id = self.request.GET.get("sex")

        if indicator_id:
            try:
                indicator = Indicator.objects.get(pk=indicator_id)
                indicator_name = indicator.name
            except Indicator.DoesNotExist:
                pass

        context["indicator_name"] = indicator_name
        
        queryset = Observation.objects.select_related("location", "indicator")

        # Fixed double-underscores for field lookups
        if geography == "national":
            queryset = queryset.filter(location__level__iexact="country")
        elif geography == "regional":
            queryset = queryset.filter(location__level__in=["regional", "region", "Regional"])
        elif geography == "zone":
            queryset = queryset.filter(location__level__iexact="zone")
        elif geography == "woreda":
            queryset = queryset.filter(location__level__iexact="woreda")

        if topic_id:
            queryset = queryset.filter(indicator__topic_id=topic_id)
        if indicator_id:
            queryset = queryset.filter(indicator_id=indicator_id)
        if year:
            queryset = queryset.filter(year=year)
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        if cause_id:
            queryset = queryset.filter(cause_id=cause_id)
        if sex_id:
            queryset = queryset.filter(sex_id=sex_id)

        # Bar chart data aggregation
        data = (
            queryset
            .values("location__name")
            .annotate(total=Sum("value"))
            .order_by("-total")
        )

        labels = [row["location__name"] for row in data if row["location__name"]]
        values = [float(row["total"]) if row["total"] is not None else 0.0 for row in data if row["location__name"]]

        context["chart_labels"] = labels
        context["chart_values"] = values

        context["data"] = [
            {
                "label": row["location__name"],
                "value": float(row["total"]) if row["total"] is not None else 0.0
            }
            for row in data if row["location__name"]
        ]

        context["show_map"] = True
        
        context["topics"] = Topic.objects.all() if 'Topic' in globals() else []
        context["indicators"] = Indicator.objects.all()
        context["years"] = Observation.objects.values_list('year', flat=True).distinct().order_by('-year')
        context["locations"] = Location.objects.all()
        context["causes"] = Cause.objects.all() if 'Cause' in globals() else []
        context["sexes"] = Sex.objects.all() if 'Sex' in globals() else []

        context["selected_geography"] = geography
        context["selected_topic"] = topic_id
        context["selected_indicator"] = indicator_id
        context["selected_year"] = year
        context["selected_location"] = location_id
        context["selected_cause"] = cause_id
        context["selected_sex"] = sex_id

        # Line chart data aggregation (fixed order_by and values_list syntax)
        linedata = (
            queryset
            .values("year")
            .annotate(total=Sum("value"))
            .order_by("year")
        )

        context["line_chart_labels"] = [str(row["year"]) for row in linedata if row["year"]]
        context["line_chart_values"] = [float(row["total"] or 0) for row in linedata if row["year"]]

        return context    
def dashboard_view(request):
    if request.method == "POST" and "excel_file" in request.FILES:
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                process_excel_upload(request.FILES["excel_file"])
                messages.success(request, "Data uploaded successfully.")
                return redirect("dashboard")
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Invalid upload.")

    queryset = Observation.objects.select_related(
        "indicator",
        "location",
        "cause",
        "sex",
        "facility_category",
        "age_group",
    ).all()

    geography = request.GET.get("geography", "regional")
    topic_id = request.GET.get("topic") or None
    indicator_id = request.GET.get("indicator") or None
    year = request.GET.get("year") or None
    location_id = request.GET.get("location") or None
    cause_id = request.GET.get("cause") or None
    sex_id = request.GET.get("sex") or None
    age_group_id = request.GET.get("age_group") or None
    facility_category_id = request.GET.get("facility_category") or None

    selected_indicator = None
    viz_config = None
    enabled_filters = []
 
    if indicator_id:
            try:
                selected_indicator = (
                    Indicator.objects
                    .get(pk=indicator_id)
                )
                viz_config = VisualizationConfig.objects.filter(indicator=selected_indicator).first()

                if viz_config:
                    enabled_filters = viz_config.filters or []

            except Indicator.DoesNotExist:
                pass
    if topic_id:
        queryset = queryset.filter(
            indicator__topic_id=topic_id
        )

    if indicator_id:
        queryset = queryset.filter(
            indicator_id=indicator_id
        )
 
    if geography == "national":
        queryset = queryset.filter(
            location__level__iexact="country"
        )
    elif geography == "regional":
        queryset = queryset.filter(
            location__level__in=[
                "regional",
                "region"
            ]
        )
    # elif geography == "zone":
    #     queryset = queryset.filter(
    #         location__level__iexact="zone"
    #     )
    # elif geography == "woreda":
    #     queryset = queryset.filter(
    #         location__level__iexact="woreda"
    #     ) 
    if year:
        queryset = queryset.filter(year=year)

    if location_id:
        queryset = queryset.filter(location_id=location_id)

    if cause_id:
        queryset = queryset.filter(cause_id=cause_id)

    if sex_id:
        queryset = queryset.filter(sex_id=sex_id)

    if age_group_id:
        queryset = queryset.filter(age_group_id=age_group_id)

    if facility_category_id:
        queryset = queryset.filter(facility_category_id=facility_category_id)

    metrics = queryset.aggregate(
        total_value=Sum("value"),
        average_value=Avg("value"),
        total_records=Count("id"),
        latest_year=Max("year"),
    )

 
    chart_data = {}

    if selected_indicator:
        viz_config = VisualizationConfig.objects.filter(indicator=selected_indicator).first()
        
        if not viz_config:
            class DefaultConfig:
                chart_type = selected_indicator.default_chart_type or "line"
                x_axis = "year"   
                indicator = selected_indicator
            viz_config = DefaultConfig()

        try:
            chart_data = build_chart_data(
                queryset,
                viz_config
            )
        except Exception as e:
            print("Chart generation error:", e)
            chart_data = {}

    map_queryset = (
        queryset
        .values(
            "location__id",
            "location__name"
        )
        .annotate(
            value=Avg("value")
        )
    )

    map_data = [
        {
            "id": item["location__id"],
            "name": item["location__name"],
            "value": float(item["value"])
            if item["value"] is not None
            else 0.0,
        }
        for item in map_queryset
    ]

    rankings = queryset.order_by("-value")[:20]
    table_records = queryset.order_by("-year")[:100]

    topics = Topic.objects.all()
    indicators = Indicator.objects.all()
    locations = Location.objects.all()
    sexes = Sex.objects.all()
    causes = Cause.objects.all()
    facility_categories = FacilityCategory.objects.all()
    age_groups = AgeGroup.objects.all()

    years = (
        Observation.objects
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    geojson_url = "/api/geojson/"

    context = {
        "upload_form": ExcelUploadForm(),
        "topics": topics,
        "indicators": indicators,
        "locations": locations,
        "sexes": sexes,
        "causes": causes,
        "facility_categories": facility_categories,
        "age_groups": age_groups,
        "years": years,
        "records": table_records,
        "rankings": rankings,
        "chart_data": json.dumps(chart_data),
        "map_data": json.dumps(map_data),
        "enabled_filters": enabled_filters,
        "geojson_url": geojson_url,
        "selected_topic": topic_id,
        "selected_indicator": indicator_id,
        "selected_year": year,
        "selected_location": location_id,
        "selected_cause": cause_id,
        "selected_sex": sex_id,
        "selected_age_group": age_group_id,
        "selected_facility_category": facility_category_id,
        "selected_geography": geography,
        "total_value": metrics["total_value"] or 0,
        "average_value": metrics["average_value"] or 0,
        "total_records": metrics["total_records"] or 0,
        "latest_year": metrics["latest_year"] or "-",
    }

    return render(
        request,
        "analytics_hub/dashboard.html",
        context,
    )
def analysis_data(request, slug):

    if slug == "disease_trends":
        return disease_trends(request)

    elif slug == "regional_comparison":
        return regional_comparison(request)

    elif slug == "gender_disease_distribution":
        return gender_distribution(request)
    
def ai_chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Simple intelligent mock response or integrate OpenAI/LLM here
            if 'disease' in user_message or 'malaria' in user_message:
                response_text = "Based on current GBD records, malaria cases peak heavily during seasonal rainy months in tropical regions."
            elif 'region' in user_message:
                response_text = "You can filter specific regions using the multi-select dropdown at the top of your dashboard."
            else:
                response_text = f"I received your query: '{user_message}'. VizHub AI assistant is ready to help analyze your GBD health metrics!"
                
            return JsonResponse({'status': 'success', 'reply': response_text})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def my_view(request):
    current_locale = get_language()           # Gets language from current thread
    request_locale = request.LANGUAGE_CODE    # Gets language bound to the request
    
    print(f"Current Active Locale: {current_locale}")
    
    # You can pass it into context dictionaries if needed
    return render(request, 'analytics_hub/dashboard.html', {'active_locale': current_locale})

def custom_login_view(request):
    return render(request, 'analytics_hub/auth_login.html')

def custom_signup_view(request):
    return render(request, 'analytics_hub/auth_signup.html')



########



# def dashboard_view(request):
#     # Handle Excel Upload POST request
#     if request.method == 'POST' and 'excel_file' in request.FILES:
#         form = ExcelUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']
#             try:
#                 df = pd.read_excel(excel_file)
#                 records_to_create = []
#                 for _, row in df.iterrows():
#                     rec_date = row.get('date')
#                     if pd.isna(rec_date):
#                         rec_date = datetime.now().date()
#                     else:
#                         rec_date = pd.to_datetime(rec_date).date()

#                     records_to_create.append(
#                         GBDRecord(
#                             topic=str(row.get('topic', 'covid_19')),
#                             date=rec_date,
#                             disease=str(row.get('disease', '')) if pd.notna(row.get('disease')) else None,
#                             age_group=str(row.get('age_group', '')) if pd.notna(row.get('age_group')) else None,
#                             facility=str(row.get('facility', '')) if pd.notna(row.get('facility')) else None,
#                             location=str(row.get('location', 'Addis Ababa')),
#                             metric_value=float(row.get('metric_value', 0.0)) if pd.notna(row.get('metric_value')) else 0.0
#                         )
#                     )
#                 GBDRecord.objects.bulk_create(records_to_create)
#                 messages.success(request, f"Successfully imported {len(records_to_create)} records from Excel!")
#                 return redirect('dashboard')
#             except Exception as e:
#                 messages.error(request, f"Error processing Excel file: {e}")
#         else:
#             messages.error(request, "Invalid file format uploaded.")

#     # Fetch distinct options for dynamic filtering lists
#     topics = GBDRecord.TOPIC_CHOICES
#     diseases = GBDRecord.objects.exclude(disease__isnull=True).exclude(disease='').values_list('disease', flat=True).distinct()
#     age_groups = GBDRecord.objects.exclude(age_group__isnull=True).exclude(age_group='').values_list('age_group', flat=True).distinct()
#     facilities = GBDRecord.objects.exclude(facility__isnull=True).exclude(facility='').values_list('facility', flat=True).distinct()
#     locations = GBDRecord.objects.exclude(location__isnull=True).exclude(location='').values_list('location', flat=True).distinct()

#     # Capture multi-select checkboxes and parameters from GET query string
#     selected_topics = request.GET.getlist('topic')
#     selected_diseases = request.GET.getlist('disease')
#     selected_ages = request.GET.getlist('age_group')
#     selected_facilities = request.GET.getlist('facility')
#     selected_locations = request.GET.getlist('location')
#     date_from = request.GET.get('date_from', '')
#     date_to = request.GET.get('date_to', '')

#     # Base Queryset
#     queryset = GBDRecord.objects.all()

#     # Apply dynamic filtering matching checkboxes and criteria
#     if selected_topics:
#         queryset = queryset.filter(topic__in=selected_topics)
#     if selected_diseases:
#         queryset = queryset.filter(disease__in=selected_diseases)
#     if selected_ages:
#         queryset = queryset.filter(age_group__in=selected_ages)
#     if selected_facilities:
#         queryset = queryset.filter(facility__in=selected_facilities)
#     if selected_locations:
#         queryset = queryset.filter(location__in=selected_locations)
#     if date_from:
#         queryset = queryset.filter(date__gte=date_from)
#     if date_to:
#         queryset = queryset.filter(date__lte=date_to)

#     # Compute figures summary
#     total_metrics = queryset.aggregate(total=Sum('metric_value'))['total'] or 0.0

#     context = {
#         'records': queryset[:100],
#         'total_metrics': total_metrics,
#         'topics': topics,
#         'diseases': diseases,
#         'age_groups': age_groups,
#         'facilities': facilities,
#         'locations': locations,
#         'selected_topics': selected_topics,
#         'selected_diseases': selected_diseases,
#         'selected_ages': selected_ages,
#         'selected_facilities': selected_facilities,
#         'selected_locations': selected_locations,
#         'date_from': date_from,
#         'date_to': date_to,
#         'upload_form': ExcelUploadForm(),
#     }
#     return render(request, 'analytics_hub/dashboard.html', context)

# #########
# def upload_view(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         try:
#             process_excel_upload(request.FILES['excel_file'])
#             messages.success(request, "Data successfully appended to the GBD database!")
#         except Exception as e:
#             messages.error(request, f"Error processing file: {e}")
#     return redirect('dashboard')

from django.shortcuts import redirect
from django.contrib import messages
# import process_excel_upload from wherever you define it (e.g., utils.py or views.py)

def upload_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            process_excel_upload(request.FILES['excel_file'])
            messages.success(request, "Data successfully appended to the GBD database!")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
    return redirect('dashboard')
# #########

def download_pdf_report(request):
    selected_regions = request.GET.getlist('regions')
    selected_facilities = request.GET.getlist('facilities')
    selected_diseases = request.GET.getlist('diseases')
    selected_age = request.GET.get('age_group', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')

    records = GBDRecord.objects.all()
    if selected_regions:
        records = records.filter(region__in=selected_regions)
    if selected_facilities:
        records = records.filter(facility__in=selected_facilities)
    if selected_diseases:
        records = records.filter(disease__in=selected_diseases)
    if selected_age:
        records = records.filter(age_group=selected_age)
    if year_from and year_from.isdigit():
        records = records.filter(year__gte=int(year_from))
    if year_to and year_to.isdigit():
        records = records.filter(year__lte=int(year_to))

    filter_params = {
        'regions': ", ".join(selected_regions) if selected_regions else 'All',
        'facilities': ", ".join(selected_facilities) if selected_facilities else 'All',
        'diseases': ", ".join(selected_diseases) if selected_diseases else 'All',
        'year_range': f"{year_from or 'Start'} to {year_to or 'Present'}",
        'age_group': selected_age or 'All',
    }

    pdf_file = generate_gbd_pdf_report(records, filter_params)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="VizHub_GBD_Report.pdf"'
    return response
