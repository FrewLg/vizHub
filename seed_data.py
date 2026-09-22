from decimal import Decimal
from analytics_hub.models import (
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
    AgeGroup,
    DimensionType,
    DimensionValue,
    Analysis,
    FilterDefinition,
)

def run():
    print("Seeding full VizHub sample data including dimensions and analytics...")

    # 1. Topics
    covid_topic, _ = Topic.objects.get_or_create(
        name="COVID-19 Surveillance",
        description="Daily and cumulative tracking of COVID-19 cases and deaths."
    )
    maternal_topic, _ = Topic.objects.get_or_create(
        name="Maternal and Child Health",
        description="Indicators related to maternal mortality, facility delivery, and child care."
    )

    # 2. Indicators
    ind_cases, _ = Indicator.objects.get_or_create(
        code="COVID_CUM_CASES",
        defaults={
            "topic": covid_topic,
            "name": "Cumulative Confirmed COVID-19 Cases",
            "description": "Total confirmed cases recorded over time.",
            "unit": "Cases",
            "default_chart_type": "line",
            "supports_map": True,
        }
    )

    ind_anc, _ = Indicator.objects.get_or_create(
        code="ANC_4_VISITS",
        defaults={
            "topic": maternal_topic,
            "name": "Antenatal Care (ANC) 4+ Visits",
            "description": "Percentage of pregnant women receiving at least 4 ANC visits.",
            "unit": "%",
            "default_chart_type": "bar",
            "supports_map": True,
        }
    )

    # 3. Visualization Configs
    VisualizationConfig.objects.get_or_create(
        indicator=ind_cases,
        defaults={
            "chart_type": "line",
            "x_axis": "year",
            "filters": ["year", "location", "sex"],
            "map_enabled": True,
        }
    )

    VisualizationConfig.objects.get_or_create(
        indicator=ind_anc,
        defaults={
            "chart_type": "bar",
            "x_axis": "location",
            "filters": ["year", "location", "facility_category"],
            "map_enabled": True,
        }
    )

    # 4. Locations (Ethiopia and Regions)
    country, _ = Location.objects.get_or_create(
        code="ETH",
        defaults={"name": "Ethiopia", "level": "country"}
    )
    
    region_aa, _ = Location.objects.get_or_create(
        code="ET-AA",
        defaults={"name": "Addis Ababa", "level": "region", "parent": country}
    )

    region_or, _ = Location.objects.get_or_create(
        code="ET-OR",
        defaults={"name": "Oromia", "level": "region", "parent": country}
    )

    # Add dummy geometry records
    LocationGeometry.objects.get_or_create(location=country, defaults={"geojson": {"type": "Polygon", "coordinates": []}})
    LocationGeometry.objects.get_or_create(location=region_aa, defaults={"geojson": {"type": "Polygon", "coordinates": []}})
    LocationGeometry.objects.get_or_create(location=region_or, defaults={"geojson": {"type": "Polygon", "coordinates": []}})

    # 5. Demographics and Categories
    sex_male, _ = Sex.objects.get_or_create(name="Male")
    sex_female, _ = Sex.objects.get_or_create(name="Female")

    cause_covid, _ = Cause.objects.get_or_create(name="SARS-CoV-2")
    
    facility_hospital, _ = FacilityCategory.objects.get_or_create(name="Hospital")
    
    source_moh, _ = DataSource.objects.get_or_create(
        name="Ministry of Health Routine Report",
        organization="MOH Ethiopia",
        url="https://www.moh.gov.et"
    )

    age_group_all, _ = AgeGroup.objects.get_or_create(name="All Ages", code="all")

    # 6. Dimension Types and Values (Flexible dimensions)
    dim_wealth, _ = DimensionType.objects.get_or_create(name="Wealth Quintile")
    DimensionValue.objects.get_or_create(dimension_type=dim_wealth, name="Poorest")
    DimensionValue.objects.get_or_create(dimension_type=dim_wealth, name="Richest")

    dim_urban, _ = DimensionType.objects.get_or_create(name="Residence Type")
    DimensionValue.objects.get_or_create(dimension_type=dim_urban, name="Urban")
    DimensionValue.objects.get_or_create(dimension_type=dim_urban, name="Rural")

    # 7. Analysis and Filter Definitions
    analysis_maternal, _ = Analysis.objects.get_or_create(
        slug="maternal-dashboard",
        defaults={"title": "Maternal Health Performance Analytics"}
    )

    FilterDefinition.objects.get_or_create(
        analysis=analysis_maternal,
        field_name="year",
        defaults={"filter_type": "year"}
    )
    FilterDefinition.objects.get_or_create(
        analysis=analysis_maternal,
        field_name="gender",
        defaults={"filter_type": "gender"}
    )

    # 8. Observations (Test data points for 2024 and 2025)
    Observation.objects.get_or_create(
        indicator=ind_cases,
        location=region_aa,
        year=2024,
        sex=sex_male,
        cause=cause_covid,
        defaults={
            "value": Decimal("25.600000"),
            "lower_bound": Decimal("24.000000"),
            "upper_bound": Decimal("27.200000"),
            "data_source": source_moh,
            "age_group": age_group_all
        }
    )

    Observation.objects.get_or_create(
        indicator=ind_cases,
        location=region_aa,
        year=2025,
        sex=sex_male,
        cause=cause_covid,
        defaults={
            "value": Decimal("25.000000"),
            "lower_bound": Decimal("23.500000"),
            "upper_bound": Decimal("26.500000"),
            "data_source": source_moh,
            "age_group": age_group_all
        }
    )

    print("Successfully seeded all VizHub models including Dimension Types and Analyses!")

if __name__ == "__main__":
    run()