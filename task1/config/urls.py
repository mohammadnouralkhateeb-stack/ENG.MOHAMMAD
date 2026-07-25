from django.urls import path
from blog.views import generate_post_view

urlpatterns = [
    path("posts/generate/", generate_post_view), 
]