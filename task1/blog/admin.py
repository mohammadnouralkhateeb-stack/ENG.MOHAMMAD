# from django.contrib import admin
# from .models import User, Category, Post, Comment  # ✅ استيراد موديلاتك أنت فقط

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'phone_number', 'is_active', 'created_at')
#     search_fields = ('name', 'phone_number')
#     list_filter = ('is_active', 'created_at')


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'author', 'category', 'created_at')
#     search_fields = ('title', 'content')
#     list_filter = ('created_at', 'is_published')


# admin.site.register(Category)
# admin.site.register(Comment)
# # هون سجلناهم بطريقة كلاسيكية لانهم بسيطات و ما في داعي للتفصيل و الزخرفة 