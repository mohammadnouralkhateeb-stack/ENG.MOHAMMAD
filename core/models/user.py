from django.contrib.auth.hashers import check_password as verify_password
from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return verify_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name