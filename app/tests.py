from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from .models import Application


class SimpleAppTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='simple_user', password='qwerty', email='')
        User.objects.create_superuser(username='super_user', password='admin', email='')

        public_application = Application(
            author=User.objects.get(username='simple_user'),
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            zip_file=SimpleUploadedFile('public.zip', b'Test'),
            is_private=False
        )
        another_public_application = Application(
            author=User.objects.get(username='super_user'),
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            zip_file=SimpleUploadedFile('public.zip', b'Test'),
            is_private=False
        )
        private_application = Application(
            author=User.objects.get(username='simple_user'),
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            zip_file=SimpleUploadedFile('private.zip', b'Test'),
            is_private=True
        )
        public_application.save()
        another_public_application.save()
        private_application.save()

        self.client = Client()

    def test_file_extension_is_zip(self):
        """
        Uploading another filename extension than .zip is illegal
        therefore no object should be created if that's the case.
        """
        self.client.login(username='simple_user', password='qwerty')
        self.client.post('/upload/', {
            'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            'zip_file': SimpleUploadedFile('test.zip', b'test')
        })
        self.assertEqual(len(Application.objects.all()), 4)

        self.client.post('/upload/', {
            'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            'zip_file': SimpleUploadedFile('test.exe', b'test')
        })
        self.assertEqual(len(Application.objects.all()), 4)

    def test_can_update_others_applications(self):
        """
        An user can only update his applications,
        if he tries to access another user application update page,
        he should be redirected.
        An anonymous user can't upload an applicaton.
        """
        # Anonymous
        response = self.client.get('/upload/')
        self.assertRedirects(response, '/signin/', status_code=302, target_status_code=200)

        response = self.client.get('/edit/1/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/edit/2/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/edit/3/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        # User1
        self.client.login(username='simple_user', password='qwerty')

        response = self.client.get('/edit/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/edit/2/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/edit/3/')
        self.assertEqual(response.status_code, 200)

        # User 2
        self.client.login(username='super_user', password='admin')

        response = self.client.get('/edit/1/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/edit/2/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/edit/3/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_log_in_system(self):
        """
        Try different redirect or accesses depending of the user privileges/status.
        """
        response = self.client.get('/signout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.login(username='admin', password='admin')
        self.assertEqual(response, False)

        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/signout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.login(username='simple_user', password='qwerty')
        self.assertEqual(response, True)

        response = self.client.get('/signup/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/signin/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/signout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)
