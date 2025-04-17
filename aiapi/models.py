from django.db import models

class Questions(models.Model):
    topic = models.CharField(max_length=255, unique=True)
    questions = models.JSONField(default=list)

    def __str__(self):
        return self.topic
