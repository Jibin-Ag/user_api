# # urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload/', views.upload_csv, name='upload_csv'),
# ]
from django.urls import path
from .views import UploadCSVAPIView

urlpatterns = [
    path('upload-csv/', UploadCSVAPIView.as_view(), name='upload-csv'),
]
