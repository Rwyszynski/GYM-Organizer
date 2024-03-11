"""
URL configuration for GYM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from excercises import views

from rest_framework import routers
from excercises.views import UserApi


router = routers.DefaultRouter()
router.register('api', UserApi)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('aboutus/', views.AboutUs.as_view(), name='about_us'),
    path('createuser/', views.CreateUserView.as_view(), name='create_user'),
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('show_plan/', views.ShowUserPlan.as_view(), name='show_user_plan'),
    path('show_workouts/', views.AllWorkouts.as_view(), name='show_all_workouts'),
    path('show_warmups/', views.AllWarmups.as_view(), name='show_all_warmups'),
    path('show_stretchings/', views.AllStretchings.as_view(),
         name='show_all_stretch'),
    path('plan_details/<int:planed_id>/',
         views.MyPlanDetails.as_view(), name='plan_details'),

    path('form/', views.Form.as_view(), name='form'),
    path('Add_workout_to_plan.as_view/',
         views.Add_workout_to_plan.as_view(), name='add_workout_to_plan'),
    path('details/', views.Details.as_view(), name='details'),
    path('edit_plan/', views.Edit_plan.as_view(), name='edit_plan'),
    path('', include(router.urls)),
]
