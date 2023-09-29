from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from atomic_habits.models import Habit

User = get_user_model()


class HabitSerializerValidator(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('atomic_habits:public_habits')
        self.maxDiff = None

    def test_PublicHabitsListAPIView(self):
        Habit.objects.create(time='2023-09-26T15:25:59.503734Z', action='Делать курсовую', place='Дом',
                             is_published=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
