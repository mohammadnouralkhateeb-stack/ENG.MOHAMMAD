"""DRF serializers for the HR models and the AI action endpoints."""
from rest_framework import serializers

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]
        
class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = ["id", "title", "department", "description", "location", "posted_date", "requirements"]
        read_only_fields = ["id", "posted_date"]
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "full_name", "email", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at"]
        
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "candidate", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
        
class ScreeningResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningResult
        fields = ["id", "candidate", "job_position", "result", "created_at"]
        read_only_fields = ["id", "created_at"]
        
class InterviewQuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestionSet
        fields = [
            "id",
            "candidate",
            "job_position",
            "screening_result",
            "technical_questions",
            "behavioral_questions",
            "follow_up_questions",
            "generated_at",
        ]
        read_only_fields = ["id", "generated_at"]
        
class RunActionSerializer(serializers.Serializer):
    """Serializer for the Run Action endpoint."""
    created_at = serializers.DateTimeField(read_only=True)