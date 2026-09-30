from models import candidate, resume, result, interview_questions, job
from rest_framework import serializers


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = candidate
        fields = '__all__'
        
        
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = resume
        fields = '__all__'
        

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = result
        fields = '__all__'
        
        
class InterviewQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = interview_questions
        fields = '__all__'
        
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = job
        fields = '__all__'