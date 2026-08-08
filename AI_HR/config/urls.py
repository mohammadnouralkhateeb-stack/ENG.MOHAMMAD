"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core.views import (
    CandidateCreateAPIView,
    InterviewQuestionSetDetailAPIView,
    JobPositionCreateAPIView,
    ResumeUploadAPIView,
    ScreeningResultDetailAPIView,
)
from django.urls import path

urlpatterns = [
    path('api/job-positions/', JobPositionCreateAPIView.as_view(), name='job-position-create'),
    path('api/candidates/', CandidateCreateAPIView.as_view(), name='candidate-create'),
    path('api/resumes/', ResumeUploadAPIView.as_view(), name='resume-upload'),
    path('api/screening-results/<int:pk>/', ScreeningResultDetailAPIView.as_view(), name='screening-result-detail'),
    path('api/interview-question-sets/<int:pk>/', InterviewQuestionSetDetailAPIView.as_view(), name='interview-question-set-detail'),
]