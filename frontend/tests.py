from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from api import models


class FrontEndTests(TestCase):
    def setUp(self):
        # Create a User
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')

        self.rio_user1 = models.RioUser.objects.create(user=self.user1)
        self.rio_user2 = models.RioUser.objects.create(user=self.user2)

    def test_access_homepage(self):
        response = self.client.get(reverse('frontend:home'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '/register')
        self.assertContains(response, '/login')
        self.assertNotContains(response, 'View Keys')
        self.assertNotContains(response, '/logout')

        self.client.force_login(self.user1)
        response = self.client.get(reverse('frontend:home'))
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, '/register')
        self.assertNotContains(response, '/login')
        self.assertContains(response, 'View Keys')
        self.assertContains(response, '/logout')

    def test_register_page(self):
        response = self.client.get(reverse('frontend:register'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Create Rio User')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')

        self.client.force_login(self.user1)
        response = self.client.get(reverse('frontend:register'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/')

    def test_login_page(self):
        response = self.client.get(reverse('frontend:login'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')

        self.client.force_login(self.user1)
        response = self.client.get(reverse('frontend:login'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/')

    def test_all_users_page(self):
        response = self.client.get(reverse('frontend:users'))
        self.assertEquals(response.status_code, 200)
        # We should see all users
        self.assertContains(response, self.rio_user1.username())
        self.assertContains(response, self.rio_user2.username())

        # Make rio_user2 private and we should not see it now
        self.rio_user2.private = True
        self.rio_user2.save()

        response = self.client.get(reverse('frontend:users'))
        self.assertEquals(response.status_code, 200)
        # We should not see all users, rio_user2 should be hidden
        self.assertContains(response, self.rio_user1.username())
        self.assertNotContains(response, self.rio_user2.username())

        # Login user1 and make them staff
        self.client.force_login(self.user1)
        self.user1.is_staff = True
        self.user1.save()

        response = self.client.get(reverse('frontend:users'))
        self.assertEquals(response.status_code, 200)
        # We should now see all rio users and user2 is private
        self.assertEquals(self.rio_user1.private, False)
        self.assertContains(response, self.rio_user1.username())
        self.assertEquals(self.rio_user2.private, True)
        self.assertContains(response, self.rio_user2.username())
        self.assertContains(response, 'Private')

    def test_user_specific_page(self):
        response = self.client.get(reverse('frontend:users', kwargs={'username': 'testuser2'}))
        self.assertEquals(response.status_code, 200)
        # We should see the user
        self.assertContains(response, self.rio_user2.username())

        # Make rio_user2 private and we should not see it now
        self.rio_user2.private = True
        self.rio_user2.save()

        response = self.client.get(reverse('frontend:users', kwargs={'username': 'testuser2'}))
        self.assertEquals(response.status_code, 200)
        # We should not see all users, rio_user2 should show they do not exist
        self.assertContains(response, 'does not exist')

        # Login user1 and make them staff
        self.client.force_login(self.user1)
        self.user1.is_staff = True
        self.user1.save()

        response = self.client.get(reverse('frontend:users'))
        self.assertEquals(response.status_code, 200)
        # We should now see all user2 and user2 is private
        self.assertEquals(self.rio_user2.private, True)
        self.assertContains(response, self.rio_user2.username())
        self.assertContains(response, 'Private')

# Create tests for actual registration and login
