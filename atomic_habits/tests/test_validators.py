from django.core.exceptions import ValidationError
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
        self.url = reverse('atomic_habits:habits-list')
        self.habit = Habit.objects.create(time='2023-09-26T15:25:59.503734Z', action='Делать курсовую', place='Дом')

    def test_related_habit_and_award_forbidden(self):
        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом", "award": "award",
                "related_habit": self.habit.pk}
        response = self.client.post(self.url, data=data)
        expected_response = "{'non_field_errors': [ErrorDetail(string='Нельзя одновременно указывать связанную привычку и награду.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_pleasant_habit_and_related_habit_forbidden(self):
        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом",
                "related_habit": self.habit.pk, "is_pleasant_habit": True}
        response = self.client.post(self.url, data=data)
        expected_response = "{'non_field_errors': [ErrorDetail(string='У приятной привычки не может быть вознаграждения или связанной привычки.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_related_habit_can_not_be_non_pleasant_habit(self):
        data = {"time": "2023-09-26T15:25:59.503734Z", "action": "Делать курсовую", "place": "Дом",
                "related_habit": self.habit.pk}
        response = self.client.post(self.url, data=data)
        expected_response = "{'non_field_errors': [ErrorDetail(string='В связанные привычки можно добавлять только приятные привычки.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_periodicity_is_more_than_seven(self):
        habit = Habit.objects.create(time='2023-09-26T15:25:59.503734Z', action='Делать курсовую', place='Дом',
                                     periodicity=8)
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_time_to_complete_is_more_120(self):
        habit = Habit.objects.create(time='2023-09-26T15:25:59.503734Z', action='Делать курсовую', place='Дом',
                                     time_to_complete=200)
        with self.assertRaises(ValidationError):
            habit.full_clean()
