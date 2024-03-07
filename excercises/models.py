from django.db import models
from django.contrib.auth.models import User


class Quotes(models.Model):
    quote = models.TextField(max_length=300, unique=True)
    author = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.quote}'


class Excercises(models.Model):
    name = models.Charfield(max_length=32)
    amount = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    burned_calories = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} x {self.amount} for {self.time} seconds'


class Strech(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=200)
    excercise = models.ManyToManyField(Excercises, through='WarmupExcercises')

    def __str__(self):
        return f'{self.title}'


intensity_choice = (
    (1, 'for_begginers')
    (2, 'for begginers but more advenced')
    (3, 'for advanced ones')
)


class Workout(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=200)
    excercises = models.ManyToManyField(
        Excercises, through='WorkoutExcercises')
    intensity = models.IntegerField(choices=intensity_choice)
    warmup = models.ForeignKey(WarmUp, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Stretching(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=200)
    excercises = models.ManyToManyField(
        Excercises, through='StretchingExcercises')

    def __str__(self):
        return f'{self.title}'
