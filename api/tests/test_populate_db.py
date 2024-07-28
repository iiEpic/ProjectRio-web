from django.test import TestCase
from api import models


class PopulateDBTestCase(TestCase):
    def setUp(self):
        self.apple = 1
        # Create a Rio User
        # self.rio_user_home = models.RioUser.objects.create(
        #     username='HomePlayer',
        #     email='homeplayer@email.com',
        #     password='my_awesome_password'
        # )
        # self.rio_user_away = models.RioUser.objects.create(
        #     username='AwayPlayer',
        #     email='awayplayer@email.com',
        #     password='my_awesome_password'
        # )

    def test_animals_can_speak(self):
        self.assertEquals(self.apple, 1)

