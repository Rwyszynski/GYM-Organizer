from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Exercises


class UserApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: Exercises
        fields = ['name', 'amount', 'time', 'burned_calories']
