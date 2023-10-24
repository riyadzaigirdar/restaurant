import json
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from restaurant.models import RestaurantModel, MenuModel, MenuVoteModel

USER_LOGIN_URL = reverse('user:login')

RESTAURANT_URL = reverse('restaurant:restaurant')
MENU_URL = reverse('restaurant:menu')
MENU_VOTE_URL = reverse('restaurant:menu-vote')
MENU_TODAY_URL = reverse('restaurant:menu_today')
VOTE_RESULT = reverse('restaurant:vote_result')


def create_employee(params):
    return get_user_model().objects.create_employee(**params)


def create_superuser(params):
    return get_user_model().objects.create_superuser(**params)


def get_superuser_token(client):
    super_user = create_superuser({
        "name": 'riyad_admin',
        "email": "riyad_admin@gmail.com",
        "password": "123456"
    })

    login_res = client.post(
        USER_LOGIN_URL, {"email": super_user.email, "password": '123456'})

    token = login_res.data['data']['token']

    return token


def get_employee_token(client):
    super_user = create_employee({
        "name": 'riyad_employee',
        "email": "riyad_employee@gmail.com",
        "password": "123456"
    })

    login_res = client.post(
        USER_LOGIN_URL, {"email": super_user.email, "password": '123456'})

    token = login_res.data['data']['token']

    return token


class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_restaurant(self):
        new_restaurant = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        token = get_superuser_token(self.client)

        res = self.client.get(RESTAURANT_URL, HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['message'],
                         'Successfully listed all restaurant')

        self.assertIn('data', res.data)

        self.assertEqual(len(res.data['data']), 1)

        self.assertEqual(new_restaurant.name, res.data['data'][0]['name'])

        self.assertEqual(new_restaurant.location,
                         res.data['data'][0]['location'])

    def test_create_restaurant(self):
        token = get_superuser_token(self.client)

        res = self.client.post(
            RESTAURANT_URL, data=json.dumps({"name": "restaurant 1", "location": "restaurant location"}), content_type='application/json', HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['message'],
                         'Successfully created restaurant')

        self.assertEqual(res.data['data']['name'], 'restaurant 1')

        self.assertEqual(res.data['data']['location'], 'restaurant location')

    def test_create_menu(self):
        token = get_superuser_token(self.client)

        new_restaurant = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        payload = {"name": "menu 1 for sunday", "description": "menu 1 sunday description",
                   "price": 450, "restaurant": new_restaurant.id}

        res = self.client.post(MENU_URL, json.dumps(payload),
                               content_type='application/json', HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['message'], 'Successfully created menu')

        self.assertIn('data', res.data)

        self.assertEqual(res.data['data']['name'], 'menu 1 for sunday')

        self.assertEqual(res.data['data']['description'],
                         'menu 1 sunday description')

        self.assertEqual(res.data['data']['price'],
                         '450.00')

        self.assertEqual(
            res.data['data']['restaurant_detail']['id'], new_restaurant.id)

    def test_list_menu(self):
        token = get_superuser_token(self.client)

        new_restaurant = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        payload1 = {"name": "menu 1 for sunday", "description": "menu 1 sunday description",
                    "price": 450, "restaurant": new_restaurant.id}

        self.client.post(MENU_URL, json.dumps(payload1),
                         content_type='application/json', HTTP_AUTHORIZATION=token)

        res = self.client.get(MENU_URL, HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn('message', res.data)

        self.assertIn('data', res.data)

        self.assertEqual(len(res.data['data']), 1)

    def test_todays_menu(self):
        token1 = get_superuser_token(self.client)
        token2 = get_employee_token(self.client)

        new_restaurant1 = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        new_restaurant2 = RestaurantModel.objects.create(
            name='restatunt 2', location='restaurant 2 location')

        payload1 = {"name": "menu 1 for sunday", "description": "menu 1 sunday description",
                    "price": 450, "restaurant": new_restaurant1.id}

        payload2 = {"name": "menu 2 for sunday", "description": "menu 2 sunday description",
                    "price": 550, "restaurant": new_restaurant2.id}

        self.client.post(MENU_URL, json.dumps(payload1),
                         content_type='application/json', HTTP_AUTHORIZATION=token1)

        self.client.post(MENU_URL, json.dumps(payload2),
                         content_type='application/json', HTTP_AUTHORIZATION=token1)

        res = self.client.get(MENU_TODAY_URL, HTTP_AUTHORIZATION=token2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['message'],
                         "Successfully listed today's menus")

        self.assertEqual(len(res.data['data']), 2)

    def test_create_vote(self):
        new_restaurant = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        menu_name = 'Sushi'
        menu_description = 'sushi menu description'
        menu_price = 12

        menu = MenuModel.objects.create(
            name=menu_name, description=menu_description, price=menu_price, restaurant=new_restaurant)

        token = get_employee_token(self.client)

        payload = {
            "menu": menu.id,

        }

        res = self.client.post(MENU_VOTE_URL, json.dumps(payload),
                               content_type='application/json', HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['message'], 'Successfully voted for menu')

        self.assertEqual(res.data['data']['menu'], menu.id)

    def test_todays_winer(self):
        new_restaurant1 = RestaurantModel.objects.create(
            name='restatunt 1', location='restaurant 1 location')

        new_restaurant2 = RestaurantModel.objects.create(
            name='restatunt 2', location='restaurant 2 location')

        menu_name1 = 'Sushi'
        menu_description1 = 'sushi menu description'
        menu_price1 = 12

        menu_name2 = 'Sushi 2'
        menu_description2 = 'sushi 2 menu description'
        menu_price2 = 34

        menu1 = MenuModel.objects.create(
            name=menu_name1, description=menu_description1, price=menu_price1, restaurant=new_restaurant1)

        menu2 = MenuModel.objects.create(
            name=menu_name2, description=menu_description2, price=menu_price2, restaurant=new_restaurant2)

        token = get_employee_token(self.client)

        payload1 = {
            "menu": menu1.id,
        }

        current_date = timezone.now()

        self.client.post(MENU_VOTE_URL,  data=json.dumps(payload1),
                         content_type='application/json', HTTP_AUTHORIZATION=token)

        res = self.client.get(
            VOTE_RESULT, QUERY_STRING=f'date={current_date.date()}', HTTP_AUTHORIZATION=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(
            res.data['message'], 'Successfully generated vote result for today')

        self.assertEqual(len(res.data['data']), 2)

        self.assertEqual(res.data['data'][0]['menu_id'], menu1.id)
