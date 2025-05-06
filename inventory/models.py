from django.db import models
from decimal import Decimal

class Drug(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    quantity = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return self.name

   


