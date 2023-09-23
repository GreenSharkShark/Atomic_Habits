from rest_framework import viewsets, generics
from atomic_habits.models import Habit
from atomic_habits.paginators import HabitPaginator
from atomic_habits.seriallizers import HabitsSerializer


class HabitsViewSet(viewsets.ModelViewSet):
    """ Класс для механизма CRUD для модели Habit """

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = []
    pagination_class = HabitPaginator

# реализовать регистрацию для привязки пользователя
    # def perform_create(self, serializer):
    #     new_habit = serializer.save()
    #     new_habit.user = self.request.user
    #     new_habit.save()


class PublicHabitsListAPIView(generics.ListAPIView):
    """ Отдельный клас для выведения списка только публичных привычек """
    serializer_class = HabitsSerializer
    queryset = Habit.objects.filter(is_published=True)

