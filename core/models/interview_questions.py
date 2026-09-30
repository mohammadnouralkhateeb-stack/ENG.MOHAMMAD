from django.db import models

class interview_questions(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    question_text = models.TextField()
    
    def __str__(self):
        return f"{self.job.title} - {self.question_text[:50]}..."