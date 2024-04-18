from django import forms
from .models import ExcelFile


class ExcelForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']