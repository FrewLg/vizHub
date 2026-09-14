import pandas as pd
from django.db import transaction
from django.utils.text import slugify
from .models import Observation, Topic, Indicator, Location, Cause, Sex, FacilityCategory, AgeGroup

def process_excel_upload(excel_file):
    df = pd.read_excel(excel_file)
    observations_to_create = []

    with transaction.atomic():
        for _, row in df.iterrows():
            # 1. Resolve Topic
            topic_obj, _ = Topic.objects.get_or_create(
                name=str(row['topic']).strip()
            )

            # 2. Resolve Indicator with unique code
            ind_name = str(row['indicator']).strip()
            ind_base_code = slugify(ind_name) or 'indicator'
            ind_code = ind_base_code
            ind_counter = 1
            while Indicator.objects.filter(code=ind_code).exclude(name=ind_name).exists():
                ind_code = f"{ind_base_code}-{ind_counter}"
                ind_counter += 1

            indicator_obj, _ = Indicator.objects.get_or_create(
                topic=topic_obj,
                name=ind_name,
                defaults={'code': ind_code}
            )

            # 3. Resolve Location with unique code
            loc_name = str(row['location']).strip()
            loc_base_code = slugify(loc_name) or 'location'
            loc_code = loc_base_code
            loc_counter = 1
            while Location.objects.filter(code=loc_code).exclude(name=loc_name).exists():
                loc_code = f"{loc_base_code}-{loc_counter}"
                loc_counter += 1

            location_obj, _ = Location.objects.get_or_create(
                name=loc_name,
                defaults={
                    'code': loc_code,
                    'level': str(row.get('geography', 'regional')).strip().lower()
                }
            )

            # 4. Resolve Optional Foreign Keys
            cause_name = str(row.get('cause', 'None')).strip()
            cause_obj = None if cause_name.lower() in ['none', 'nan', ''] else Cause.objects.get_or_create(name=cause_name)[0]

            sex_name = str(row.get('sex', 'Both')).strip()
            sex_obj = Sex.objects.get_or_create(name=sex_name)[0] if sex_name.lower() not in ['nan', ''] else None

            fac_cat_name = str(row.get('facility_category', 'Hospital')).strip()
            facility_category_obj = FacilityCategory.objects.get_or_create(name=fac_cat_name)[0] if fac_cat_name.lower() not in ['nan', ''] else None

            # 5. Parse metrics
            year_val = int(row['year']) if pd.notna(row.get('year')) else 2024
            val = float(row['value']) if pd.notna(row.get('value')) else 0.0
            lower = float(row['lower_bound']) if pd.notna(row.get('lower_bound')) else None
            upper = float(row['upper_bound']) if pd.notna(row.get('upper_bound')) else None

            age_group_name = str(row.get('age_group', 'All Ages')).strip()
            age_group_obj = None
            if age_group_name.lower() not in ['nan', '', 'none']:
                age_base_code = slugify(age_group_name) or 'age'
                age_code = age_base_code
                counter = 1
                while AgeGroup.objects.filter(code=age_code).exclude(name=age_group_name).exists():
                    age_code = f"{age_base_code}-{counter}"
                    counter += 1
                age_group_obj, _ = AgeGroup.objects.get_or_create(
                    name=age_group_name,
                    defaults={'code': age_code}
                )
 
            observations_to_create.append(
                Observation(
                    indicator=indicator_obj,
                    location=location_obj,
                    cause=cause_obj,
                    sex=sex_obj,
                    facility_category=facility_category_obj,
                    year=year_val,
                    value=val,
                    age_group=age_group_obj,
                    lower_bound=lower,
                    upper_bound=upper
                )
            )

        Observation.objects.bulk_create(observations_to_create, ignore_conflicts=True)