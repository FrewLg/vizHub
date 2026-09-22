from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from django import forms
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
)

def environment_callback(request):
    return ["Production", "success"]

class ObservationAdminForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        lower = cleaned_data.get("lower_bound")
        upper = cleaned_data.get("upper_bound")

        if lower is not None and upper is not None and lower > upper:
            raise forms.ValidationError(
                "Lower bound cannot be greater than upper bound."
            )
        return cleaned_data


class LocationGeometryInline(admin.StackedInline):
    model = LocationGeometry
    can_delete = False
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "topic", "default_chart_type", "supports_map", "supports_national", "supports_regional")
    list_filter = ("topic", "default_chart_type", "supports_map", "supports_national", "supports_regional")
    search_fields = ("code", "name", "description", "unit")
    list_per_page = 25


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "level", "parent", "is_active")
    list_filter = ("level", "is_active")
    search_fields = ("name", "code")
    autocomplete_fields = ("parent",)
    inlines = [LocationGeometryInline]


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")


@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "url")
    search_fields = ("name", "organization", "citation")


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    form = ObservationAdminForm
    list_display = (
        "indicator",
        "location",
        "year",
        "sex",
        "cause",
        "value",
        "lower_bound",
        "upper_bound",
    )
    list_filter = (
        "year",
        "indicator__topic",
        "sex",
        "facility_category",
        "data_source",
    )
    search_fields = (
        "indicator__name",
        "indicator__code",
        "location__name",
        "location__code",
    )
    autocomplete_fields = (
        "indicator",
        "location",
        "sex",
        "cause",
        "facility_category",
        "data_source",
    )
    actions_list = ["add_observation"]

    def add_observation(self, request):
        return redirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_add"
            )
        )

    add_observation.short_description = "Add New Observation"
    list_per_page = 50


@admin.register(VisualizationConfig)
class VisualizationConfigAdmin(admin.ModelAdmin):
    list_display = (
        "indicator",
        "chart_type",
        "map_enabled",
        "national_enabled",
        "regional_enabled",
        "ranking_enabled",
    )
    list_filter = (
        "chart_type",
        "map_enabled",
        "national_enabled",
        "regional_enabled",
        "ranking_enabled",
    )
    autocomplete_fields = ("indicator",)


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 1


@admin.register(DimensionType)
class DimensionTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    inlines = [DimensionValueInline]