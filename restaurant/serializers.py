from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from restaurant.models import RestaurantModel, MenuModel, MenuVoteModel


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = ['id', 'name', 'location']
        read_only_fields = ['id']


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = MenuModel
        fields = ['id', 'name', 'description',
                  'price', 'restaurant', 'created_at']
        read_only_fields = ['id', 'created_at']


class MenuVoteSerializer(serializers.ModelSerializer):
    menu_detail = MenuSerializer(source='menu', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = MenuVoteModel
        fields = ['id', 'menu', 'user', 'menu_detail', 'user_detail']
        read_only_fields = ['id']
