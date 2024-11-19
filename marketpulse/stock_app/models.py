from django.db import models

# Create your models here.

class StockCache(models.Model):
    company = models.CharField(max_length=50)
    duration = models.IntegerField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.duration} years"

