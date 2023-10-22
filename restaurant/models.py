from django.db import models
from django.conf import settings


class RestaurantModel(models.Model):
    name = models.CharField(max_length=500, null=False)
    location = models.TextField(null=True)

    class Meta:
        db_table = "restaurant"

    def __str__(self):
        return self.name


class MenuModel(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    restaurant = models.ForeignKey(RestaurantModel,
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return self.name


class MenuVoteModel(models.Model):
    menu = models.ForeignKey(MenuModel,
                             on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'menu_vote'

    def __str__(self):
        return f"vote id {self.id}"
