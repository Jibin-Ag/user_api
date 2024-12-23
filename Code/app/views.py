# from django.shortcuts import render

# # Create your views here.
# # views.py
# import csv
# from io import StringIO
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import User
# from .serializers import UserSerializer

# @api_view(['POST'])
# def upload_csv(request):
#     if 'csv_file' not in request.FILES:
#         return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

#     csv_file = request.FILES['csv_file']
    
#     # Validate the file extension
#     if not csv_file.name.endswith('.csv'):
#         return Response({'error': 'Only CSV files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

#     # Parse the CSV file
#     try:
#         file_content = csv_file.read().decode('utf-8')
#         reader = csv.DictReader(StringIO(file_content))
#     except Exception as e:
#         return Response({'error': 'Error reading CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

#     success_count = 0
#     reject_count = 0
#     rejected_records = []

#     for row in reader:
#         data = {
#             'name': row.get('name'),
#             'email': row.get('email'),
#             'age': row.get('age')
#         }

#         serializer = UserSerializer(data=data)
        
#         if serializer.is_valid():
#             try:
#                 # Save user record, ensuring unique emails
#                 User.objects.create(**serializer.validated_data)
#                 success_count += 1
#             except Exception as e:
#                 reject_count += 1
#                 rejected_records.append({
#                     'row': row,
#                     'error': str(e)
#                 })
#         else:
#             reject_count += 1
#             rejected_records.append({
#                 'row': row,
#                 'errors': serializer.errors
#             })
    
#     # Respond with a summary of the results
#     response_data = {
#         'success_count': success_count,
#         'reject_count': reject_count,
#         'rejected_records': rejected_records
#     }

#     return Response(response_data, status=status.HTTP_200_OK)
import csv
from io import StringIO
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UploadCSVAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return Response({"error": "Invalid file. Only CSV files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        file_data = file.read().decode('utf-8')
        csv_data = csv.DictReader(StringIO(file_data))

        saved_count = 0
        rejected_count = 0
        errors = []

        for row_number, row in enumerate(csv_data, start=1):
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved_count += 1
                except Exception as e:
                    errors.append({
                        "row": row_number,
                        "error": f"Duplicate email or database error: {str(e)}"
                    })
                    rejected_count += 1
            else:
                errors.append({
                    "row": row_number,
                    "errors": serializer.errors
                })
                rejected_count += 1

        return Response({
            "saved_records": saved_count,
            "rejected_records": rejected_count,
            "errors": errors
        }, status=status.HTTP_200_OK)
