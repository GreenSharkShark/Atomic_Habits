from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User

NULlABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    time = models.DateTimeField(verbose_name='время')
    action = models.TextField(verbose_name='действие')
    place = models.CharField(max_length=250, verbose_name='место')
    award = models.CharField(max_length=250, verbose_name='награда', **NULlABLE)
    is_published = models.BooleanField(default=False, verbose_name='признак публичности', **NULlABLE)
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки', **NULlABLE)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULlABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель привычки',
                             related_name='habit', **NULlABLE)
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность в днях',
                                                   validators=[MaxValueValidator(7)], **NULlABLE)
    time_to_complete = models.PositiveSmallIntegerField(default=60, validators=[MaxValueValidator(120)],
                                                        verbose_name='время на выполнение', **NULlABLE)
