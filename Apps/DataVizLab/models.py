from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os


def validate_csv_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    if ext.lower() != '.csv':
        raise ValidationError('El archivo debe ser un archivo CSV.')


class CSVFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', validators=[validate_csv_file_extension])


