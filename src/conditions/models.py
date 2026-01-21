from django.db import models

# Create your models here.
class Condition(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    physical = models.IntegerField(null=True, blank=True)
    mental = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_absent = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
