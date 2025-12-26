from django.db import models

# Create your models here.

class Condition(models.Model):
    record_date = models.DateField()
    physical = models.IntegerField()
    mental = models.IntegerField()
    memo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.record_date} / P:{self.physical} M:{self.mental}"
