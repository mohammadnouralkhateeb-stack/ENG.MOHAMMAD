from django.contrib import admin

# Register your models here.

"""Register HR models so they can be managed from the Django admin site."""

from core.models import candidate, interview_questions, job, resume, result

@admin.register(candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone")
    search_fields = ("full_name", "email")

@admin.register(resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "file", "uploaded_at")

@admin.register(result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "job_position", "score", "recommendation", "generated_at")
    list_filter = ("recommendation",)

@admin.register(interview_questions)
class InterviewQuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "job_position", "generated_at")

@admin.register(job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at")
    search_fields = ("title",)