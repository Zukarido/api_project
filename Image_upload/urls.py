from django.urls import path, include
from .views import FileUploadView

urlpatterns = [
    path('', FileUploadView.as_view(), name='home' ),
]
