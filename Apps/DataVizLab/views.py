from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CSVFile
from .forms import CSVForm

import pandas as pd


@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save(commit=False)
            csv_file.user = request.user            # Asignar el usuario actual al campo user
            csv_file.save()
            df = pd.read_csv(csv_file.file.path)
            columns = df.columns
            id = csv_file.id
            return render(request, 'DataVizLab/column_select.html', {'columns': columns, 'csv_file_id': id})
    else:
        form = CSVForm()
    return render(request, 'DataVizLab/upload_csv.html', {'form': form})
