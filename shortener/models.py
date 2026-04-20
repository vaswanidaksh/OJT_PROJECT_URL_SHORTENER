from django.db import models
from django.utils import timezone
from .utils import generate_short_code

# Create your models here.

class ShortURL(models.Model):
    # unique=True ensures the same long URL cannot be shortened twice —
    # the view will look up existing entries before creating a new one.
    original_url = models.URLField(unique=True, help_text="The long URL to shorten")
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Expiry defaults to 30 days from creation
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Generate code if it doesn't exist
        if not self.short_code:
            self.short_code = generate_short_code()
            # Ensure uniqueness
            while ShortURL.objects.filter(short_code=self.short_code).exists():
                self.short_code = generate_short_code()
        
        # Set default expiry if not provided (30 days)
        if not self.expires_at:
             self.expires_at = timezone.now() + timezone.timedelta(days=30)
             
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"