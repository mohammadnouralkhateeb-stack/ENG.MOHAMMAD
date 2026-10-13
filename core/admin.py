from django.contrib import admin

from core.models.job_details import JobDetails
from core.models.resume import Resume
from core.models.search_result import SearchResult
from core.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name")
    search_fields = ("user_name",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "resume_file")
    search_fields = ("user__user_name",)
    list_select_related = ("user",)


@admin.register(JobDetails)
class JobDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "job_title", "location", "salary", "posted_date")
    search_fields = ("job_title", "location", "description")
    list_filter = ("posted_date",)


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ("id", "job_title", "company", "location", "score")
    search_fields = ("job_title", "company", "location", "description")
    list_filter = ("location",)
