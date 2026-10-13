from core.serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import SearchHistory  # (افترض أن هذا جدول سجل البحث لديك)
from core.serializers import SearchHistorySerializer

class UserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)
        
        # 1. التحقق هل المستخدم موجود أم لا
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # المستخدم موجود وكلمة المرور صحيحة
            pass
        else:
            # التحقق إذا كان الاسم موجوداً ولكن كلمة المرور خطأ، أو إنشاء حساب جديد
            try:
                user = User.objects.get(username=username)
                return Response({"error": "Incorrect password."}, status=400)
            except User.DoesNotExist:
                # إنشاء حساب جديد تلقائياً (Sign Up)
                user = User.objects.create_user(username=username, password=password)
        
        # 2. التحقق من وجود سجل بحث سابق (Search History) للمستخدم
        history_records = SearchHistory.objects.filter(user=user)
        
        if history_records.exists():
            serializer = SearchHistorySerializer(history_records, many=True)
            return Response({
                "status": "history_found",
                "user_id": user.id,
                "results": serializer.data
            })
        else:
            return Response({
                "status": "no_history",
                "user_id": user.id,
                "results": []
            })