from django.db import models
from django.utils.timezone import now

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name 

class OrderSummary(models.Model):
    date = models.DateField(default=now)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    @property
    def order_total(self):
        orderdetails = self.orderdetail_set.all()
        total = sum([details.total_price for details in orderdetails])
        return total
    
    @property
    def change(self):
        orderdetails = self.orderdetail_set.all()
        total = sum([details.total_price for details in orderdetails])
        change = self.payment_amount - total
        if total > self.payment_amount:
            return "Insufficient Amount!"
        elif self.payment_amount >= total:
            return f"₱{change}"

class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField()

    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, blank=True, null=True)
    order_summary = models.ForeignKey(OrderSummary, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Order of {self.menu_item.name}"
    
    @property
    def total_price(self):
        return self.menu_item.price * self.quantity
    
    def change(self):
        total_amount = self.menu_item.price * self.quantity
        change = self.order_summary.payment_amount - total_amount
        if total_amount > self.order_summary.payment_amount:
            return "Insufficient Amount!"
        elif self.order_summary.payment_amount > total_amount:
            return f"₱{change}"
        
