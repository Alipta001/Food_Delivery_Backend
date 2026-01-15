from django.db import models

class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    rating = models.FloatField()
    cuisine_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to="restaurants/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
