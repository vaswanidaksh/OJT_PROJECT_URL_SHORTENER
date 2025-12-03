from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import generate_short_code

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    original_url = models.URLField(max_length=2048, help_text="The long URL to shorten")
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
            while ShortURL.objects.filter(short_code=self.short_code).exists():
                self.short_code = generate_short_code()

        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
