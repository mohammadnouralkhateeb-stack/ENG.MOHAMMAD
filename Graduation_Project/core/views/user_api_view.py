from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import SearchHistory
from core.serializers import SearchHistorySerializer


class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)
        
        # Check whether the user already exists.
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # The existing user's password is valid.
            pass
        else:
            # Reject an existing username with a wrong password; otherwise create an account.
            try:
                user = User.objects.get(username=username)
                return Response({"error": "Incorrect password."}, status=400)
            except User.DoesNotExist:
                # Create a new account.
                user = User.objects.create_user(username=username, password=password)
        
        # Check whether the user has previous search history.
        history_records = SearchHistory.objects.filter(user=user).order_by("-created_at")
        token, _ = Token.objects.get_or_create(user=user)
        
        if history_records.exists():
            serializer = SearchHistorySerializer(history_records, many=True)
            return Response({
                "status": "history_found",
                "user_id": user.id,
                "token": token.key,
                "results": serializer.data
            })
        else:
            return Response({
                "status": "no_history",
                "user_id": user.id,
                "token": token.key,
                "results": []
           })
        