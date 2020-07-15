from django.test import TestCase
from note.models import Post
from django.conf import settings
from django.contrib.auth.models import User
from uuid import UUID


def is_valid_uuid(uuid_to_test):
    try:
        UUID(uuid_to_test)
        return True
    except ValueError:
        return False


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        user = User.objects.get(id=1)
        Post.objects.create(user=user, title='test title', content='test content')

    def test_verbose_name_title(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_max_length_title(self):
        post = Post.objects.get(id=1)
        title_max_length = post._meta.get_field('title').max_length
        print(title_max_length)
        self.assertEquals(title_max_length, 120)

    def test_verbose_name_content(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_get_absolute_url(self):
        author = Post.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/note/1/')

    def test_get_uuid_url(self):
        author = Post.objects.get(id=1)
        author_uuid = author.get_uuid_url().split('/')[2]
        self.assertEquals(is_valid_uuid(author_uuid), True)


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')

    def test_verbose_name_username(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        print(field_label)
        self.assertEquals(field_label, 'username')

    def test_verbose_name_password(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        print(field_label)
        self.assertEquals(field_label, 'password')
