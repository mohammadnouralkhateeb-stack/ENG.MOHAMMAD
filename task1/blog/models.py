# from django.db import models

# # =========================================================
# # USER MODEL — two ways to do it
# # =========================================================

# # ---- DEFAULT WAY (Django's built-in User) ----
# # Django already ships with a ready-made User model, so you don't
# # write it yourself. You just import it wherever you need it:
# #
# # from django.contrib.auth.models import User
# #
# # Use this when the built-in fields are enough:
# # username, email, password, first_name, last_name.


# # ---- CUSTOMIZED WAY (our own User) ----
# # When you need EXTRA fields on the user (bio, phone, avatar, ...),
# # you extend AbstractUser. You keep everything the default User has
# # and simply add your own fields on top.
# # class CustomUser(AbstractUser):
# #     bio = models.TextField(blank=True)                    # extra field
# #     phone = models.CharField(max_length=20, blank=True)   # extra field
# #
# #     def __str__(self):
# #         return self.username

# class User(models.Model):
#     phone_number = models.CharField(max_length=20, unique=True)
#     name = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f'{self.name} - {self.phone_number}'

# # NOTE: to actually USE the custom user, add this line to settings.py:
# #   AUTH_USER_MODEL = 'blog.CustomUser'
# # Do it at the START of a project (before the first migrate). If you
# # switch later, delete the old db + migration files and migrate fresh.


# # =========================================================
# # CATEGORY — a simple table (one category has many posts)
# # =========================================================
# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# # =========================================================
# # POST — the main table, now with relationships
# # =========================================================
# class Post(models.Model):
#     # ForeignKey = a "one-to-many" link: one user writes many posts.
#     #
#     # CUSTOMIZED WAY: point at settings.AUTH_USER_MODEL so this works
#     # whether you use the DEFAULT User or the CUSTOM one (best practice).
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,   # delete a user's posts with the user
#         related_name='posts',       # reverse access: user.posts.all()
#     )

#     # ---- DEFAULT WAY (point straight at the built-in User) ----
#     # author = models.ForeignKey(
#     #     'auth.User',
#     #     on_delete=models.CASCADE,
#     #     related_name='posts',
#     # )

#     category = models.ForeignKey(
#         Category,
#         on_delete=models.SET_NULL,  # keep the post even if its category is gone
#         related_name='posts',
#         null=True,
#         blank=True,
#     )

#     title = models.CharField(max_length=150)
#     content = models.TextField()
#     is_published = models.BooleanField(default=True)   # used by the "hide unpublished" rule
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# # =========================================================
# # COMMENT — another one-to-many (one post has many comments)
# # =========================================================
# class Comment(models.Model):
#     post = models.ForeignKey(
#         Post,
#         on_delete=models.CASCADE,
#         related_name='comments',
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments',
#     )
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Comment by {self.author} on "{self.post}"'