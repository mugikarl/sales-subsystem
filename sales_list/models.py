from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderDetails(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    name = models.ForeignKey(MenuItem, )