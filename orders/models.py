from django.db import models
from inventory.models import Drug

# Create your models here.
class Order(models.Model):
    customer_name  = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company_price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=100, decimal_places=2)
    
    order_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.price * self.quantity

    def get_company_price(self):
       return self.company_price * self.quantity

    def is_debtor(self):
        return self.paid_amount < self.get_total_price()

    def balance_due(self):
        return int(self.get_total_price() - self.paid_amount)

    def profit(self):
        return int(self.price - self.company_price) * self.quantity
    

        

    def __str__(self):
        return f"{self.customer_name} ordered {self.quantity} pack/packs of {self.drug} for {self.get_total_price()} and was paid {self.paid_amount} "
    


