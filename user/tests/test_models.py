import os
import jwt
from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ModelTests(TestCase):
    def test_create_new_employee(self):
        email = 'riad@gmail.com'
        name = 'riad'
        password = '1234'

        new_user = UserModel.objects.create_employee(email, name, password)

        self.assertEqual(new_user.name, name)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        self.assertEqual(new_user.role, 'employee')
        self.assertEqual(str(new_user), email)

    def test_create_new_admin(self):
        email = 'riad_admin@gmail.com'
        name = 'riad_admin'
        password = '1234'

        new_user = UserModel.objects.create_superuser(email, name, password)

        self.assertEqual(new_user.name, name)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        self.assertEqual(new_user.role, 'admin')

    def test_change_user_password(self):
        email = 'riyad@gmail.com'
        name = 'riad'
        password = 'pass1'
        new_password = 'pass2'

        new_user = UserModel.objects.create_superuser(email, name, password)
        new_user.set_password(new_password)

        self.assertTrue(new_user.check_password(new_password))

    def test_create_token(self):
        email = 'riyad@gmail.com'
        name = 'riad'
        password = 'pass1'

        new_user = UserModel.objects.create_employee(email, name, password)

        token = new_user.create_token()

        decoded_user = jwt.decode(token, os.environ.get(
            'JWT_SECRET'), algorithms="HS256")

        self.assertEqual(decoded_user['email'], email)
        self.assertEqual(decoded_user['name'], name)
        self.assertEqual(decoded_user['id'], new_user.id)
