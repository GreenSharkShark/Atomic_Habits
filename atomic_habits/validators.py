from rest_framework.validators import ValidationError
from atomic_habits.models import Habit


class HabitSerializerValidator:

    def __init__(self, data: dict):
        self.related_habit = data.get('related_habit')
        self.is_pleasant_habit = data.get('is_pleasant_habit')
        self.award = data.get('award')

    def __call__(self, value):
        if self.related_habit and self.award:
            raise ValidationError('Нельзя одновременно указывать связанную привычку и награду.')

        if self.is_pleasant_habit and self.award or self.is_pleasant_habit and self.related_habit:
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        if self.related_habit:
            related_habit = Habit.objects.filter(pk=self.related_habit.id).first()
            if not related_habit.is_pleasant_habit:
                raise ValidationError('В связанные привычки можно добавлять только приятные привычки.')
