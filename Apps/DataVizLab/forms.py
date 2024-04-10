from django import forms
from .models import CSVFile


class CSVForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file']