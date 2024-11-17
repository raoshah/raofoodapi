from django.db import models
from django.utils import timezone

class VerifiedEmail(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    otp_expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
