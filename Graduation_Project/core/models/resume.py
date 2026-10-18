from django.db import models
from .user import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    
    def __str__(self):
        return f"Resume for {self.user.user_name}"