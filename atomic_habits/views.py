from rest_framework import viewsets, generics
from atomic_habits.models import Habit
from atomic_habits.paginators import HabitPaginator
from atomic_habits.permissions import IsOwner
from atomic_habits.seriallizers import HabitsSerializer
from rest_framework.permissions import IsAuthenticated


class HabitsViewSet(viewsets.ModelViewSet):
    """ Класс для механизма CRUD для модели Habit """

    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """ При GET запросе возвращает список объектов создателем которых является текущий пользователь """

        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Сохраняет текущего пользователя как создателя объекта """

        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class PublicHabitsListAPIView(generics.ListAPIView):
    """ Отдельный клас для выведения списка только публичных привычек """

    serializer_class = HabitsSerializer
    queryset = Habit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]

