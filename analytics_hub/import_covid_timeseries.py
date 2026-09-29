import pandas as pd

from analytics_hub.models import (
    Indicator,
    Observation,
)

ETHIOPIA_LOCATION_ID = 1

INDICATOR_MAPPING = {
    "Active Cases": "Active Cases",
    "Severe or Critical Cases": "Severe or Critical Cases",
    "Critical Cases to Active Cases proportions":
        "Critical Cases to Active Cases Proportions",
}


df = pd.read_excel("covid_timeseries.csv")
 
df.columns = [str(c).strip() for c in df.columns]

df["Date"] = pd.to_datetime(df["Date"])

created_count = 0
updated_count = 0

for _, row in df.iterrows():

    obs_date = row["Date"].date()

    for excel_column, indicator_name in INDICATOR_MAPPING.items():

        if excel_column not in df.columns:
            continue

        value = row[excel_column]

        if pd.isna(value):
            continue

        indicator, _ = Indicator.objects.get_or_create(
            name=indicator_name
        )

        observation, created = Observation.objects.update_or_create(
            indicator=indicator,
            location_id=ETHIOPIA_LOCATION_ID,
            year=obs_date.year,
            date=obs_date,
            sex=None,
            cause=None,
            facility_category=None,
            age_group=None,
            defaults={
                "value": float(value),
            }
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

print(
    f"Created: {created_count}, Updated: {updated_count}"
)