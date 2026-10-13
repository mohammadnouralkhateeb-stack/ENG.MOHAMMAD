from core.service import run_pipeline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers.job_details_serializer import JobDetailsSerializer
from core.serializers.search_result_serializer import SearchResultSerializer
from core.serializers.resume_serializer import ResumeSerializer
from django.db import transaction

class SaveAndRunPipeline(APIView):
    def post(self, request):
        resume_serializer = ResumeSerializer(data=request.data)
        job_details_serializer = JobDetailsSerializer(data=request.data)
        resume_is_valid = resume_serializer.is_valid()
        job_details_is_valid = job_details_serializer.is_valid()
        if not resume_is_valid or not job_details_is_valid:
            return Response(
                {
                    "resume": resume_serializer.errors,
                    "job_details": job_details_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_results = run_pipeline(
            resume_serializer.validated_data["resume_file"],
            job_details_serializer.validated_data,
        )
        search_result_serializer = SearchResultSerializer(
            data=search_results,
            many=True,
        )
        if not search_result_serializer.is_valid():
            return Response(
                search_result_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            resume_serializer.save()
            job_details_serializer.save()
            search_result_serializer.save()

        return Response(
            search_result_serializer.data,
            status=status.HTTP_201_CREATED,
        )