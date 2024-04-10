from django.contrib.auth.models import User
from django.test import TestCase

from .models import CSVFile


class CSVFileModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='testemail',
                                             password='testpassword')

    def test_create_valid_instance(self):
        csv_file = CSVFile.objects.create(user=self.user, file='test.csv')
        self.assertIsNotNone(csv_file)
        self.assertEqual(csv_file.user, self.user)
        self.assertEqual(csv_file.file.name, 'test.csv')

    def test_csv_file_not_valid(self):
        with self.assertRaises(ValueError):
            csv_file = CSVFile.objects.create(user=self.user, file='test.txt')

    def tearDown(self):
        # Limpiar después de las pruebas eliminando los objetos creados
        CSVFile.objects.all().delete()
        User.objects.all().delete()

