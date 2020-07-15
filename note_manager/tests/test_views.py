from django.test import TestCase
from note.models import Post
from django.contrib.auth.models import User


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        user = User.objects.get(id=1)
        Post.objects.create(user=user, title='test title', content='test content')

    def test_homepage(self):
        response = self.client.get('/note/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
