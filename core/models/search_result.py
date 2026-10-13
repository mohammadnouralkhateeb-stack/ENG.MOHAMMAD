from django.db import models

class SearchResult(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    description = models.TextField()
    score = models.FloatField()
    link = models.URLField(max_length=200)
    
    def __str__(self):
        return f"{self.job_title} at {self.company} - {self.location} (Score: {self.score})"