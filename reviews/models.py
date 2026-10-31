from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    username = models.CharField(max_length=100)

    review_text = models.TextField()

    rating = models.IntegerField()

    sentiment = models.CharField(
        max_length=20,
        blank=True
    )

    is_fake = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.product.name}"


class MonthlyReport(models.Model):
    month = models.CharField(max_length=20)

    positive_count = models.IntegerField(default=0)

    negative_count = models.IntegerField(default=0)

    neutral_count = models.IntegerField(default=0)

    def __str__(self):
        return self.month