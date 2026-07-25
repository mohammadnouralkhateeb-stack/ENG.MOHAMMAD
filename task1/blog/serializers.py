from rest_framework import serializers # هون الهدف من السيريالايزرز هو اظهار البيانات في الداشبورد على شكل ملفات جيسون
from .models import User, Category, Post, Comment

# 1. Serializer للمستخدمين
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'is_active', 'created_at']


# 2. Serializer للأقسام
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# 3. Serializer للمقالات
class PostSerializer(serializers.ModelSerializer):
    # إظهار بيانات الكاتب والقسم كاملة عند الاستعلام (GET)
    author_details = UserSerializer(source='author', read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'title', 
            'content', 
            'is_published', 
            'author', 
            'author_details', 
            'category', 
            'category_details', 
            'created_at'
        ]


# 4. Serializer للتعليقات
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at']