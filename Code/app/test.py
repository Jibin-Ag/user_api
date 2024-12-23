# # tests.py
# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import User
# import io
# import csv

# class CSVUploadTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#     def create_csv_file(self, data):
#         """Helper method to create a CSV file."""
#         csv_file = io.StringIO()
#         writer = csv.DictWriter(csv_file, fieldnames=['name', 'email', 'age'])
#         writer.writeheader()
#         writer.writerows(data)
#         csv_file.seek(0)
#         return csv_file

#     def test_upload_valid_csv(self):
#         data = [
#             {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
#             {'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
#         ]
#         csv_file = self.create_csv_file(data)

#         response = self.client.post('/upload/', {'csv_file': csv_file}, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['success_count'], 2)
#         self.assertEqual(response.data['reject_count'], 0)

#     def test_upload_invalid_csv(self):
#         data = [
#             {'name': '', 'email': 'invalid_email', 'age': 300},  # Invalid data
#             {'name': 'John', 'email': 'john@example.com', 'age': 27},
#         ]
#         csv_file = self.create_csv_file(data)

#         response = self.client.post('/upload/', {'csv_file': csv_file}, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['success_count'], 1)
#         self.assertEqual(response.data['reject_count'], 1)
#         self.assertIn('errors', response.data['rejected_records'][0])

#     def test_upload_duplicate_email(self):
#         User.objects.create(name='Alice', email='alice@example.com', age=25)

#         data = [
#             {'name': 'Bob', 'email': 'alice@example.com', 'age': 30},  # Duplicate email
#             {'name': 'Charlie', 'email': 'charlie@example.com', 'age': 35},
#         ]
#         csv_file = self.create_csv_file(data)

#         response = self.client.post('/upload/', {'csv_file': csv_file}, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['success_count'], 1)
#         self.assertEqual(response.data['reject_count'], 1)
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO

class UploadCSVAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_upload_valid_csv(self):
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Smith,jane@example.com,25"
        file = BytesIO(csv_content.encode('utf-8'))
        file.name = 'test.csv'

        response = self.client.post('/api/users/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saved_records'], 2)
        self.assertEqual(response.data['rejected_records'], 0)

    def test_upload_invalid_csv(self):
        csv_content = "name,email,age\nJohn Doe,invalid-email,30\nJane Smith,jane@example.com,13\n mathew,mathew@gmail.com,130"
        file = BytesIO(csv_content.encode('utf-8'))
        file.name = 'test.csv'

        response = self.client.post('/api/users/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saved_records'], 1)
        self.assertEqual(response.data['rejected_records'], 2)

