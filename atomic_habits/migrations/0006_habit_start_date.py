# Generated by Django 4.2.5 on 2023-09-25 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atomic_habits', '0005_remove_habit_is_related_habit'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='время и дата начала'),
        ),
    ]