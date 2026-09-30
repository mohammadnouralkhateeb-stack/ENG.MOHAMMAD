from django.db import models

class result(models.Modle):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title} - {'Passed' if self.passed else 'Failed'}"