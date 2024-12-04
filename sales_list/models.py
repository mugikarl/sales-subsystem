from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name 

class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order_summary = models

    def __str__(self):
        return f"Order of {self.menu_item.name} on {self.date}"
    
    def total_price(self):
        return self.menu_item.price * self.quantity
    
    def change(self):
        total_amount = self.menu_item.price * self.quantity
        change = self.payment_amount - total_amount
        if total_amount > self.payment_amount:
            return "Insufficient Amount!"
        elif self.payment_amount > total_amount:
            return f"₱{change}"
        
