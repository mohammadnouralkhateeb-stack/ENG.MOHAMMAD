from django.db import models

class JobDetails(models.Model):
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title