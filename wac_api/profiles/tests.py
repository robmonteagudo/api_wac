# Create your tests here.
from PIL import Image
import tempfile
import json

from django.test import TestCase

import json

from rest_framework.test import APIClient
from rest_framework import status

from profiles.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        user = Profile(
            email='testing@robertomonteagudo.es',
            first_name='Testing',
            last_name='Testing',
            avatar="/media/users/file.jpg"
        )
        user.set_password('admin123')
        user.save()

        client = APIClient()
        response = client.post(
            '/profiles/login/', {
                'email': 'testing@robertomonteagudo.es',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

    def test_login_user(self):
        client = APIClient()
        response = client.post(
            '/profiles/login/', {
                'email': 'testing@robertomonteagudo.es',
                'password': 'admin123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = json.loads(response.content)
        self.assertIn('access_token', result)

    def test_wrong_login_user(self):
        client = APIClient()
        response = client.post(
            '/profiles/login/', {
                'email': 'testing@robertomonteagudo.es',
                'password': 'admin345',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {
                             "non_field_errors": [
                                 "Credentials are not valid. Check email and password"
                             ]
                         })

    def test_edit_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        edit_user = {
            'email': 'testing@robertomonteagudo.es',
            'first_name': 'Testing',
            'last_name': 'Testing',
            'avatar': tmp_file
        }

        response = client.put(
            f'/profiles/{self.user.pk}/',
            edit_user,
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        change_password = {
            'old_password': 'admin123',
            'new_password': 'admin321'
        }

        response = client.post(
            f'/profiles/password',
            change_password,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {
                             "code": status.HTTP_200_OK,
                             "message": "Password updated successfully"
                         })

    def test_wrong_password_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        change_password = {
            'old_password': 'admin789',
            'new_password': 'admin321'
        }

        response = client.post(
            f'/profiles/password',
            change_password,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {
                             'code': status.HTTP_400_BAD_REQUEST,
                             'message': "Wrong password"
                         })
