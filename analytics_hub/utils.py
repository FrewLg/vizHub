import pandas as pd
from .models import GBDRecord

def process_excel_upload(file):
    df = pd.read_excel(file)
    
    required_columns = ['region', 'facility', 'disease', 'year', 'age_group', 'metric_value']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Excel file must contain columns: {', '.join(required_columns)}")

    records = []
    for _, row in df.iterrows():
        records.append(
            GBDRecord(
                region=str(row['region']),
                facility=str(row['facility']),
                disease=str(row['disease']),
                year=int(row['year']),
                age_group=str(row['age_group']),
                metric_value=float(row['metric_value'])
            )
        )
    
    GBDRecord.objects.bulk_create(records)
