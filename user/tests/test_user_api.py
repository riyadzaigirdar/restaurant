from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


USER_LOGIN_URL = reverse('user:login')
USER_LIST_URL = reverse('user:employee')
USER_LOGOUT_URL = reverse('user:logout')


def create_employee(params):
    return get_user_model().objects.create_employee(**params)


def create_superuser(params):
    return get_user_model().objects.create_superuser(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_login(self):
        name = 'riyad'
        email = 'riyad@gmail.com'
        password = '12345'

        create_employee({
            "name": name,
            "email": email,
            "password": password,
        })

        res = self.client.post(
            USER_LOGIN_URL, {"email": email, "password": password})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], 'Successfully generated token')
        self.assertIn('data', res.data)
        self.assertIn('token', res.data['data'])

    def test_logout(self):
        name = 'riyad'
        email = 'riyad@gmail.com'
        password = '12345'

        create_employee({
            "name": name,
            "email": email,
            "password": password,
        })

        login_res = self.client.post(
            USER_LOGIN_URL, {"email": email, "password": password})

        token = login_res.data['data']['token']

        logout_res = self.client.post(
            USER_LOGOUT_URL, content_type='application/json',
            HTTP_AUTHORIZATION=token)

        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_res.data['message'], 'Successfully logged out')
        self.assertEqual(logout_res.data['data'], None)


class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_employee_list(self):
        super_user = create_superuser({
            "name": 'riyad_admin',
            "email": "riyad_admin@gmail.com",
            "password": "123456"
        })

        create_employee({
            "name": 'riyad1',
            "email": 'riyad1@gmail.com',
            "password": '12345',
        })

        create_employee({
            "name": 'riyad2',
            "email": 'riyad2@gmail.com',
            "password": '12345',
        })

        create_employee({
            "name": 'riyad3',
            "email": 'riyad3@gmail.com',
            "password": '12345',
        })

        login_res = self.client.post(
            USER_LOGIN_URL, {"email": super_user.email, "password": '123456'})

        token = login_res.data['data']['token']

        list_res = self.client.get(
            USER_LIST_URL, content_type='application/json', HTTP_AUTHORIZATION=token)

        self.assertEqual(list_res.status_code, status.HTTP_200_OK)

        self.assertEqual(list_res.data['message'],
                         'Successfully listed all users')

        self.assertEqual(len(list_res.data['data']), 4)

    def test_employee_create(self):
        super_user = create_superuser({
            "name": 'riyad_admin',
            "email": "riyad_admin@gmail.com",
            "password": "123456"
        })

        login_res = self.client.post(
            USER_LOGIN_URL, {"email": super_user.email, "password": '123456'})

        token = login_res.data['data']['token']

        res = self.client.post(
            USER_LIST_URL, data=r'{"email": "riyad@gmail.com", "name": "riyad", "password": "12345"}', content_type='application/json', HTTP_AUTHORIZATION=token)

        self.assertEqual(res.data['message'], 'Successfully created employee')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertNotIn('password', res.data)

        self.assertEqual(res.data['data']['email'], 'riyad@gmail.com')

        self.assertEqual(res.data['data']['name'], 'riyad')

        self.assertEqual(res.data['data']['role'], 'employee')
