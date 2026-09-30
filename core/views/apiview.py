import asyncio
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# استيراد النماذج والسيريالايزرز
from core.models import candidate, resume, result, interview_questions, job
from core.serializers import (
    CandidateSerializer,
    ResumeSerializer,
    ResultSerializer,
    InterviewQuestionsSerializer,
    JobSerializer
)

# استيراد الـ Flow
from core.flow.flow import HRPipelineFlow


@api_view(['GET', 'POST'])
def process_hr_pipeline(request):
    """
    دالة تتعامل مع طلبات الـ GET والـ POST مع التحقق بواسطة السيريالايزر
    """
    
    # ----------------------------------------------------
    # 1. حالة الـ GET: استرجاع نتائج الـ Pipeline المخزنة
    # ----------------------------------------------------
    if request.method == 'GET': # هون ما بحتاج تحقق من البيانات باستخدام (is_valid) لانها مجرد استرجاع
        results_list = result.objects.all() # هون بتم استرجاع كل النتائج المخزنة في قاعدة البيانات
        serializer = ResultSerializer(results_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------------------------------------------------
    # 2. حالة الـ POST: التحقق من البيانات وتحديث الـ Flow
    # ----------------------------------------------------
    if request.method == 'POST':
        # استخدام ResumeSerializer للتحقق من بيانات السيرة الذاتية المدخلة
        resume_serializer = ResumeSerializer(data=request.data)
        
        # إجراء التحقق (Validation)
        if not resume_serializer.is_valid():
            return Response(resume_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # البيانات المفحوصة والمضمونة
        validated_data = resume_serializer.validated_data # هون بتم استخراج البيانات النظيفة من السيريالايزر بعد التحقق منها

        try:
            # تهيئة الـ Flow
            flow = HRPipelineFlow()

            # تعبئة الـ State بالبيانات النظيفة من السيريالايزر
            flow.state.candidate_resume = validated_data.get('content', '')  
            flow.state.job_title = request.data.get('job_title', '')
            flow.state.job_description = request.data.get('job_description', '')
            flow.state.required_skills = request.data.get('required_skills', '')

            # تشغيل الـ Flow
            pipeline_output = asyncio.run(flow.kickoff_async())

            # إرجاع النتيجة
            return Response({
                "status": "success",
                "output": pipeline_output
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )