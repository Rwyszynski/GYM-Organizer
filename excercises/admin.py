from django.contrib import admin

from excercises.models import *

admin.site.register(Quotes)
admin.site.register(Exercises)
admin.site.register(Strech)
admin.site.register(Workout)
admin.site.register(Stretching)
admin.site.register(Diet)

admin.site.register(MyPlan)
admin.site.register(WorkoutInPlan)
admin.site.register(StretchingInPlan)
admin.site.register(WarmupExercises)
admin.site.register(WorkoutExercises)
admin.site.register(StretchingExercises)
