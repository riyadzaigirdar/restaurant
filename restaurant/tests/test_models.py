from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurant.models import RestaurantModel, MenuModel, MenuVoteModel

UserModel = get_user_model()


def sample_employee(email='riyad@gmail.com', name='riyad', password='12345'):
    return UserModel.objects.create_employee(email, name, password)


def sample_admin(email='riyadadmin@gmail.com', name='riyadadmin', password='12345'):
    return UserModel.objects.create_superuser(email, name, password)


def sample_restaunrant(restaurant_name='restaurant name', restaurant_location='dhaka, bangladesh'):
    return RestaurantModel.objects.create(
        name=restaurant_name, location=restaurant_location)


class ModelTests(TestCase):
    def test_create_restaurant(self):
        restaurant_name = 'restaurant name 1'
        restaurant_location = 'restaurant location'

        new_restaurant = RestaurantModel.objects.create(
            name=restaurant_name, location=restaurant_location)

        self.assertEqual(new_restaurant.name, restaurant_name)
        self.assertEqual(new_restaurant.location, restaurant_location)

    def test_create_restaurant_menu(self):
        restaurant = sample_restaunrant()
        menu_name = 'Sushi'
        menu_description = 'sushi menu description'
        menu_price = 12

        menu = MenuModel.objects.create(
            name=menu_name, description=menu_description, price=menu_price, restaurant=restaurant)

        self.assertEqual(menu.name, menu_name)
        self.assertEqual(menu.description, menu_description)
        self.assertEqual(menu.price, menu_price)

    def test_menu_vote(self):
        user = sample_employee()
        restaurant = sample_restaunrant()

        menu_name = 'Sushi'
        menu_description = 'sushi menu description'
        menu_price = 12
        menu = MenuModel.objects.create(
            name=menu_name, description=menu_description, price=menu_price, restaurant=restaurant)

        menu_vote = MenuVoteModel.objects.create(user=user, menu=menu)

        self.assertEqual(menu_vote.user.name, user.name)
        self.assertEqual(menu_vote.menu.name, menu_name)
