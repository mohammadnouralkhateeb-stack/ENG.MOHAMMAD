from django.db import models

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='job_positions')
    description = models.TextField()
    location = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)   
    requirements = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.title