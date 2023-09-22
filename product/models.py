from django.db import models
import uuid


from django.db import models


class Category(models.Model):
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.product_name
