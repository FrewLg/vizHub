from django.template.loader import render_to_string
from weasyprint import HTML

def generate_gbd_pdf_report(records, filter_params):
    """
    Generates a professional PDF report from filtered GBD records using Weasyprint.
    """
    total_records = records.count()
    
    context = {
        'records': records[:100],  # Include up to 100 rows in the report
        'total_records': total_records,
        'filter_params': filter_params,
    }
    
    # Render report template to string
    html_content = render_to_string('analytics_hub/pdf_report.html', context)
    
    # Compile HTML to PDF bytes
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes
