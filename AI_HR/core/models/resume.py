from django.db import models


class Resume(models.Model):
    candidate = models.OneToOneField('Candidate', on_delete=models.CASCADE, related_name='resume_record')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.candidate.full_name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"