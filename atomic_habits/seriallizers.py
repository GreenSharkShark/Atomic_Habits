from rest_framework import serializers
from atomic_habits.models import Habit
from atomic_habits.validators import HabitSerializerValidator


class HabitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        validator = HabitSerializerValidator(data)
        validator(data)

        return data
