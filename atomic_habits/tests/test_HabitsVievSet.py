from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from atomic_habits.models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.client.force_authenticate(user=self.user)

    def test_post(self):
        """ Тест создания объекта"""

        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом"}
        url = reverse('atomic_habits:habits-list')
        response = self.client.post(url, data=data)
        expected_data = {'id': response.data['id'], 'time': '2023-09-26T15:25:59.503734Z', 'action': 'Делать курсовую',
                         'place': 'Дом', 'award': None, 'is_published': False, 'is_pleasant_habit': False,
                         'periodicity': 1, 'time_to_complete': 60, 'related_habit': None, 'user': self.user.pk}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_get(self):
        """ Тест получения списка объектов"""

        url = reverse('atomic_habits:habits-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """ Тест получения конкретного объекта"""

        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом", "user": self.user}
        habit = Habit.objects.create(**data)
        url = reverse('atomic_habits:habits-detail', kwargs={'pk': habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """ Тест удаления объекта"""

        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом", "user": self.user}
        habit = Habit.objects.create(**data)
        url = reverse('atomic_habits:habits-detail', kwargs={'pk': habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        """ Тест изменения объекта"""

        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом",
                "user": self.user}
        habit = Habit.objects.create(**data)
        url = reverse('atomic_habits:habits-detail', kwargs={'pk': habit.pk})
        new_data = {"place": "Не дом"}
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
