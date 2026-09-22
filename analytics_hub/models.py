#from django.db import models
from django.utils import timezone
from django.db import models

#class GBDRecord(models.Model):
#    TOPIC_CHOICES = [
 #       ('covid_19', 'COVID-19 Data Analytics & Modelling Platform'),
  #      ('geospatial_vis', 'Geospatial Visualization Platform'),
   #     ('childhood_mortality', 'Childhood Mortality Indicators Trend Analysis'),
    #    ('child_diarrhea', 'Child Health Analysis - Prevalance & Treatment of Diarrhea'),
     #   ('child_fever', 'Child Health Analysis - Prevalance & Treatment of Fever'),
      #  ('child_ari', 'Child Health Analysis - Prevalance & Treatment of Acute Respiratory Infection'),
       # ('fertility_trend_nat', 'Trends of Fertility Rate for National'),
#        ('total_fertility_rates', 'Total Fertility Rates'),
 #       ('general_fertility_rates', 'General Fertility Rates'),
  ##      ('age_specific_fertility', 'Age-specific Fertility Rates'),
#        ('vaccination_12_23', 'Vaccination Coverage for Age 12 - 23 Months'),
 #       ('anc_visits', 'Antenatal Care Visits for Pregenancy'),
  #      ('skilled_birth', 'Skilled Birth Attendance During Delivery'),
   #     ('first_pnc', 'First Postnatal Checkup'),
    #    ('delivery_facility', 'Delivery in Health Facility'),
     #   ('exclusive_breastfeeding', 'Exclusive Breastfeeding'),
#        ('early_breastfeeding', 'Early Initiation of Breastfeeding'),
 #       ('child_malnutrition', 'Levels of Child Malnutrition'),
  #      ('perinatal_mortality', 'Perinatal Mortality Rate, Number of Still Birth & Early Neonatal Death Analysis'),
   #     ('emonc_assessment', 'Emergency Maternal Obstetric Newborn Care Facility Service Assesment Analysis'),
    #    ('climate_health', 'Climate and Health Data Visualization'),
     #   ('sdg_hstp_tracker', 'Health Related SDG & HSTP-II Tracker'),
      #  ('bod_life_expectancy', 'Life Expectancy at birth Ethiopia 2019(BOD)'),
       # ('bod_total_fertility', 'Total Fertility Rate in Ethiopia(BOD)'),
#        ('bod_sdi', 'Socio-Demographic Index (SDI) in Ethiopia(BOD)'),
 #       ('bod_maternal_mortality', 'Maternal Mortality Rate in Ethiopia(BOD)'),
  #      ('bod_under5_mortality', 'Under 5 Mortality Rate in Ethiopia(BOD)'),
   #     ('bod_ncd_premature', 'Premature Mortality from NCD in Ethiopia(BOD)'),
    #    ('bod_injury_mortality', 'Mortality Rate from All Types of Injuries in Ethiopia(BOD)'),
     #   ('bod_malaria_mortality', 'Malaria Mortality Rate in Ethiopia(BOD)'),
      #  ('bod_malaria_incidence', 'Malaria Incidence Rate in Ethiopia(BOD)'),
       # ('bod_cause_premature', 'Cause of Premature Mortality in Ehtiopia(BOD)'),
#    ]
#
 #   topic = models.CharField(max_length=100, choices=TOPIC_CHOICES)
  #  date = models.DateField(default=timezone.now) # Allows safe automated population
   # disease = models.CharField(max_length=100, blank=True, null=True)
    #age_group = models.CharField(max_length=50, blank=True, null=True)
#    facility = models.CharField(max_length=100, blank=True, null=True)
 #   location = models.CharField(max_length=100, blank=True, null=True)
  #  metric_value = models.FloatField(default=0.0)
#
 #   def __str__(self):
  #      return f"{self.get_topic_display()} - {self.date} ({self.location})"
#
# from django.contrib.gis.db import models

# =========================
# Topic
# =========================

class Topic(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# =========================
# Indicator
# =========================

class Indicator(models.Model):

    CHART_TYPES = [
        ("line", "Line"),
        ("bar", "Bar"),
        ("pie", "Pie"),
        ("table", "Table"),
        ("map", "Map"),
        ("rank", "Rank"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="indicators"
    )

    code = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=500
    )

    description = models.TextField(
        blank=True
    )

    unit = models.CharField(
        max_length=100,
        blank=True
    )

    default_chart_type = models.CharField(
        max_length=20,
        choices=CHART_TYPES,
        default="line"
    )

    supports_confidence_interval = models.BooleanField(
        default=False
    )

    supports_map = models.BooleanField(
        default=False
    )

    supports_national = models.BooleanField(
        default=True
    )

    supports_regional = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    age_group = models.ForeignKey(
            'AgeGroup', 
            on_delete=models.SET_NULL, 
            null=True, 
            blank=True
        )
    def __str__(self):
        return self.name


# =========================
# Geography
# =========================

class Location(models.Model):

    LEVELS = [
        ("country", "Country"),
        ("region", "Region"),
        ("zone", "Zone"),
        ("woreda", "Woreda"),
    ]

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    level = models.CharField(
        max_length=20,
        choices=LEVELS
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================
# Geometry
# =========================
 

class LocationGeometry(models.Model):

    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        related_name="geometry"
    )

    geojson = models.JSONField(
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["location"]),
        ]

    def __str__(self):
        return self.location.name


 

class Sex(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name

 

class Cause(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


 

class FacilityCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


# =========================
# Source
# =========================

class DataSource(models.Model):

    name = models.CharField(
        max_length=255
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    url = models.URLField(
        blank=True
    )

    citation = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


# =========================
# Observation
# ========================= 
class Observation(models.Model):

    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        related_name="observations"
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="observations"
    )

    # For daily, weekly, or monthly time-series data (e.g., COVID-19 surveillance)
    date = models.DateField(
        null=True,
        blank=True
    )

    year = models.PositiveIntegerField()

    sex = models.ForeignKey(
        Sex,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    cause = models.ForeignKey(
        Cause,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    facility_category = models.ForeignKey(
        FacilityCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    data_source = models.ForeignKey(
        DataSource,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    age_group = models.ForeignKey(
        'AgeGroup', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    value = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    lower_bound = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True
    )

    upper_bound = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True
    )

    # 🚀 Catch-all for any extra columns/metadata in incoming files 
    # (e.g., wealth quintile, urban/rural, custom program flags)
    extra_attributes = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["indicator", "year"]),
            models.Index(fields=["location", "year"]),
            models.Index(fields=["indicator", "location", "year"]),
            models.Index(fields=["date"]),
        ]

        unique_together = (
            "indicator",
            "location",
            "year",
            "date",
            "sex",
            "cause",
            "facility_category",
            "age_group"
        )
 
# =========================
# Visualization Config
# =========================
class VisualizationConfig(models.Model):
    indicator = models.OneToOneField(
        Indicator,
        on_delete=models.CASCADE,
        related_name="visualization"
    )

    chart_type = models.CharField(
        max_length=20,
        choices=Indicator.CHART_TYPES
    )

    x_axis = models.CharField(
        max_length=50,
        default="year"
    )

    series_dimension = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    filters = models.JSONField(
        default=list,
        blank=True
    )

    map_enabled = models.BooleanField(default=False)

    national_enabled = models.BooleanField(default=True)

    regional_enabled = models.BooleanField(default=True)

    ranking_enabled = models.BooleanField(default=False)

    color_scheme = models.CharField(
        max_length=100,
        blank=True
    )
    
class DimensionType(models.Model):
    name = models.CharField(max_length=100)


class DimensionValue(models.Model):
    dimension_type = models.ForeignKey(
        DimensionType,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)

class AgeGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

# ///////////
class Analysis(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)

class FilterDefinition(models.Model):
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE
    )

    field_name = models.CharField(max_length=50)

    FILTER_TYPES = (
        ("year", "Year"),
        ("gender", "Gender"),
        ("age_group", "Age Group"),
        ("region", "Region"),
    )

    filter_type = models.CharField(
        max_length=20,
        choices=FILTER_TYPES
    )