from django.db import models

class job(models.Model):
    
    title = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    description = models.TextField()
    required_skills = models.TextField()
    
    def __str__(self):
        return self.title