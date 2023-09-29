from django.urls import path
from atomic_habits.apps import AtomicHabitsConfig
from atomic_habits.views import *
from rest_framework.routers import DefaultRouter


app_name = AtomicHabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitsViewSet, basename='habits')

urlpatterns = [
    path('habits-public/', PublicHabitsListAPIView.as_view(), name='public_habits'),
] + router.urls
