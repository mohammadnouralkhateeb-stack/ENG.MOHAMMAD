from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from ..serializers import CandidateSerializer 

class CandidateCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = CandidateSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            # معالجة مشكلة تكرار الإيميل (Unique Constraint) لمنع 500
            return Response(
                {"detail": "Candidate with this email already exists."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )