from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import JobPositionSerializer

class JobPositionCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = JobPositionSerializer(data=request.data)
            
            # التحقق التلقائي من الـ Serializer بما فيها required_skills
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )