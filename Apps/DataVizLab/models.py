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
    file = models.FileField(upload_to='', validators=[validate_excel_file_extension])
    encryption_key = models.BinaryField(null=True, blank=True)             # Campo para almacenar la clave de encriptación

    def save(self, *args, **kwargs):
        if self.file:
            if not self.encryption_key:                                    # Genera una nueva clave solo si no hay una clave almacenada
                self.encryption_key = Fernet.generate_key()                # Genera una clave de encriptación
            fernet = Fernet(self.encryption_key)                           # Crea un objeto Fernet con la clave generada o almacenada
            encrypted_data = fernet.encrypt(self.file.read())              # Lee el contenido del archivo, lo encripta y lo guarda en encrypted_data
            self.encrypted_file = encrypted_data                           # Asigna el contenido encriptado al campo encrypted_file
            self.original_filename = self.file.name                        # Guarda el nombre original del archivo en original_filename
            self.file.delete(save=False)                                   # Borra el archivo original después de encriptarlo
        super().save(*args, **kwargs)                                      # Llama al método save() original del modelo para guardar los datos en la base de datos

    def get_decrypted_file(self):
        if self.encrypted_file and self.encryption_key:
            fernet = Fernet(self.encryption_key)                            # Crea un objeto Fernet con la clave almacenada
            decrypted_data = fernet.decrypt(self.encrypted_file)            # Desencripta el contenido del campo encrypted_file
            return decrypted_data                                           # Devuelve el contenido desencriptado
        return None                                                         # Devuelve None si el campo encrypted_file está vacío


#  TO DO:
#Guardar la clave de encriptación en la misma base de datos que los datos encriptados puede plantear preocupaciones de seguridad
#Una mejor práctica es separar la clave de encriptación de los datos encriptados y almacenarla de forma segura
#Servicio de administración de claves (KMS): Utilizar un servicio de administración de claves como AWS Key Management Service (KMS)
# o Google Cloud Key Management Service (KMS) para almacenar y administrar las claves de encriptación de forma segura.