from rest_framework import serializers

from core.models.job_details import JobDetails


class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = "__all__"