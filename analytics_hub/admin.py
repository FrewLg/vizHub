from django import forms

from django.contrib import admin
from .models import (
    Topic,
    Indicator,
    Location,
    LocationGeometry,
    Sex,
    Cause,
    FacilityCategory,
    DataSource,
    Observation,
    VisualizationConfig,
    DimensionType,
    DimensionValue,
    AgeGroup,
    Analysis,
    FilterDefinition,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "topic", "default_chart_type", "unit")
    list_filter = ("topic", "default_chart_type", "supports_map", "supports_national", "supports_regional")
    search_fields = ("code", "name", "description")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "level", "parent", "is_active")
    list_filter = ("level", "is_active")
    search_fields = ("name", "code")
    autocomplete_fields = ["parent"]


@admin.register(LocationGeometry)
class LocationGeometryAdmin(admin.ModelAdmin):
    list_display = ("location",)
    search_fields = ("location__name", "location__code")


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)  # Added to satisfy autocomplete requirements


@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)  # Added to satisfy autocomplete requirements

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "url")
    search_fields = ("name", "organization")


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = (
        "indicator",
        "location",
        "year",
        "date",
        "sex",
        "cause",
        "value",
        "data_source",
    )
    list_filter = (
        "year",
        "indicator__topic",
        "indicator",
        "location__level",
        "sex",
        "data_source",
    )
    search_fields = (
        "indicator__name",
        "indicator__code",
        "location__name",
        "location__code",
    )
    autocomplete_fields = [
        "indicator",
        "location",
        "sex",
        "cause",
        "facility_category",
        "data_source",
        "age_group",
    ]
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("Core Parameters", {
            "fields": ("indicator", "location", "year", "date")
        }),
        ("Disaggregations & Metadata", {
            "fields": ("sex", "age_group", "cause", "facility_category", "data_source", "extra_attributes")
        }),
        ("Metrics & Bounds", {
            "fields": ("value", "lower_bound", "upper_bound")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


 

class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 1


@admin.register(DimensionType)
class DimensionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [DimensionValueInline]


class FilterDefinitionInline(admin.TabularInline):
    model = FilterDefinition
    extra = 1


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")
    inlines = [FilterDefinitionInline]

FILTER_CHOICES = [
    ("year", "Year"),
    ("sex", "Sex"),
    ("age_group", "Age Group"),
    ("location", "Location"),
    ("cause", "Disease"),
    ("facility_category", "Facility Category"),
]

class VisualizationConfigAdminForm(forms.ModelForm):
    filters = forms.MultipleChoiceField(
        choices=FILTER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = VisualizationConfig
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.filters:
            self.initial["filters"] = self.instance.filters

    def clean_filters(self):
        return self.cleaned_data["filters"]


@admin.register(VisualizationConfig)
class VisualizationConfigAdmin(admin.ModelAdmin):
    form = VisualizationConfigAdminForm

    list_display = (
        "indicator",
        "chart_type",
        "x_axis",
    )

class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 1


 