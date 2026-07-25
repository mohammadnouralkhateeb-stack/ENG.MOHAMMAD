from rest_framework.decorators import api_view
from rest_framework.response import Response
from ai.content.content_service import generate_response

@api_view(["POST"])
def generate_post_view(request):
    title = request.data.get("title")
    tone = request.data.get("tone")

    try:
        result = generate_response(title=title, tone=tone)
        return Response(result, status=200)

    except ValueError as e:
        return Response({"error": str(e)}, status=400)

    except Exception as e:
        return Response({"error": "Internal server error"}, status=500)