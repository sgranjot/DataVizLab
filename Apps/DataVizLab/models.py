from cryptography.fernet import Fernet
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os


def validate_excel_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    if ext.lower() != '.xlsx':
        raise ValidationError('El archivo debe ser un archivo XLSX.')


class ExcelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    encrypted_file = models.BinaryField()
    original_filename = models.CharField(max_length=255)                   # Almacena el nombre original del archivo
    file = models.FileField(validators=[validate_excel_file_extension])

    def save(self, *args, **kwargs):
        if self.file:
            clave = Fernet.generate_key()                                  # Genera una clave de encriptación
            fernet = Fernet(clave)                                         # Crea un objeto Fernet con la clave generada
            encrypted_data = fernet.encrypt(self.file.read())              # Lee el contenido del archivo, lo encripta y lo guarda en encrypted_data
            self.encrypted_file = encrypted_data                           # Asigna el contenido encriptado al campo encrypted_file
            self.original_filename = self.file.name                        # Guarda el nombre original del archivo en original_filename
            self.file.delete(save=False)                                   # Borra el archivo original después de encriptarlo
        super().save(*args, **kwargs)                                      # Llama al método save() original del modelo para guardar los datos en la base de datos

    def get_decrypted_file(self):
        if self.encrypted_file:
            clave = Fernet.generate_key()                                   # Genera una clave de encriptación
            fernet = Fernet(clave)                                          # Crea un objeto Fernet con la clave generada
            decrypted_data = fernet.decrypt(self.encrypted_file)            # Desencripta el contenido del campo encrypted_file
            return decrypted_data                                           # Devuelve el contenido desencriptado
        return None                                                         # Devuelve None si el campo encrypted_file está vacío


