from django.contrib import admin

from core.models import Resume
from core.models import Candidate
from core.models import JobPosition
from core.models import InterviewQuestionSet
from core.models import ScreeningResult

# Register your models here.

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'uploaded_at')
    search_fields = ('candidate__full_name',)
    list_filter = ('uploaded_at',)
    
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'application_date')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('application_date',)
    
@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'posted_date')
    search_fields = ('title', 'department__name', 'location')
    list_filter = ('department', 'location', 'posted_date')
    
@admin.register(InterviewQuestionSet)
class InterviewQuestionSetAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_position', 'generated_at')
    search_fields = ('candidate__full_name', 'job_position__title')
    list_filter = ('generated_at',)