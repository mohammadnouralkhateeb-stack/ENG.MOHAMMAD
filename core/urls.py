from django.urls import path
from .views import process_hr_pipeline

urlpatterns = [
    path('pipeline/', process_hr_pipeline, name='process_hr_pipeline'),
]