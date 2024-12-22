from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    total_spent = models.PositiveIntegerField(default=0)  # Сумма всех покупок
    discount = models.FloatField(default=0.0)  # Накопительная скидка в процентах

    def update_discount(self):
        """Обновляет скидку в зависимости от общей суммы покупок."""
        if self.total_spent >= 10000:
            self.discount = 10.0
        elif self.total_spent >= 5000:
            self.discount = 5.0
        else:
            self.discount = 0.0
        self.save()

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)