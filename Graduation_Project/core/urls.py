from django.urls import path

from .views.save_details_view import SaveAndRunPipeline
from .views.user_api_view import UserAPIView

urlpatterns = [
    path('details/', SaveAndRunPipeline.as_view(), name='save_and_run_pipeline'),
    path('user/', UserAPIView.as_view(), name='user_api'),
]
