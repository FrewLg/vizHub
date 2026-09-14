# analytics_hub/forms.py
from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Select Excel File (.xlsx)',
        widget=forms.FileInput(attrs={'class': 'block w-full text-xs text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'})
    )
