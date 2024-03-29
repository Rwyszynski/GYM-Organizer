import random
from django.shortcuts import render, redirect

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views import View

from excercises.forms import CreateUserForm, LoginForm, CreatePlanForm, AddWorkoutToPlanForm, AddStretchingToPlanForm, \
    CreateWarmUpForm, AddExercisesToWarmupForm, CreateWorkoutForm, AddExercisesToWorkoutForm, CreateStretchForm, \
    AddExercisesToStretchForm
from excercises.models import Quotes, MyPlan, WorkoutInPlan, StretchingInPlan, Workout, Strech, Stretching, Diet, \
    WarmupExercises

from rest_framework import viewsets
from .models import Exercises
from .api import UserApi


class ExerciseView(viewsets.ModelViewSet):
    queryset = Exercises.objects.all()
    serializer_class = UserApi


class Index(View):
    # tu zrób stronę tytułową

    def get(self, request):
        quotes = list(Quotes.objects.all())
        if len(quotes) > 0:
            random.shuffle(quotes)
            q1 = quotes[0]
        else:
            q1 = "Brak"
        ctx = {'q1': q1}

        return render(request, 'index.html', ctx)


class AboutUs(View):

    # tu stwórz kartę z użytkownikiem 

    def get(self, request):
        info = 'halo to ja'
        return render(request, 'abouts.html', {'helo': info})


class CreateUser(View):
    # Stwórz użytkowniak

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'form.html', {'form': form, 'info': 'Zacznij z nami'})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password_one']
            user.set_password(password)
            user.save()
            return redirect('login')
        return render(request, 'form.html', {'form': form, 'message': 'Złe dane'})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            us = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            user = authenticate(username=us, password=pd)
            if user is None:
                return render(request, 'form.html', {'form': form, 'message': 'THIS USER DOES NOT EXIST'})
            else:
                login(request, user)
                url = request.GET.get('next', 'homepage')
                return redirect(url)
        return render(request, 'form.html', {'form': form, 'message': 'Zły login lub hasło'})

class LogoutView(LoginRequiredMixin, View):
    # Strona wylogowania
    def get(self, request):
        logout(request)
        return redirect('index')


class HomepageView(LoginRequiredMixin, View):
    # Zawartość tylko dla użytkownków
    def get(self, request):
        return render(request, 'homepage.html')


class CreateYourPlan(LoginRequiredMixin):
    # Stwórz plan
    def get(self, request):
        form = CreatePlanForm()
        return render(request, 'form.html', {'form': form, 'info': 'Stwórz swoj plan'})

    def post(self, request):
        form = CreatePlanForm(request.POST)
        if form.is_valid():
            diet = form.cleaned_data['diet']
            name = form.cleaned_data['name']
            user_plan = MyPlan.objects.create(name=name, diet=diet, owner=request.user)
            return render(request, 'form.html', {'plan_added': 'Plan został dodany'})
        return render(request, 'form.html', {'form': form, 'info': 'Złe dane'})


class AddWorkoutToPlan(LoginRequiredMixin):
    # dodaj plan dla użytkownika
    def get(self, request):
        form = AddWorkoutToPlanForm()
        user = request.user
        plans = MyPlan.objects.filter(owner=user)
        form.fields['plan'].queryset = plans
        return render(request, 'form.html', {'form': form, 'info': "Dodaj ćwiczenia do planu"})

    def post(self, request):
        form = AddWorkoutToPlanForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            workout = form.cleaned_data['workout']
            plan = form.cleaned_data['hour']
            hour = form.cleaned_data['hour']
            WorkoutInPlan.objects.create(day=day, workout=workout, plan=plan, hour=hour)
            return render(request, 'form.html', {'add_train_to_plan': 'Dodano plan treningowy', 'plan': plan})
        return render(request, 'form.html', {'form': form, 'info': 'Złe dane'})


class AddStretchingToPlan(LoginRequiredMixin, View):
    # Wybierz plan

    def get(self, request):
        form = AddStretchingToPlanForm()
        user = request.user
        plans = MyPlan.objects.filter(owner=user)
        form.fields['plan'].queryset = plans
        return render(request, 'form.html', {'form': form, 'info': 'DOdaj plan rozciągania'})

    def post(self, request):
        form = AddStretchingToPlanForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            stretching = form.cleaned_data['plan']
            plan = form.cleaned_data['plan']
            hour = form.cleaned_data['plan']
            StretchingInPlan.objects.create(day=day, stretching=stretching, plan=plan, hour=hour)
            return render(request, 'form.html', {'Dodano': form, 'plan': plan})
        return render(request, 'form.html', {'form': form, 'info': 'Złe dane'})


class ShowUserPlan(LoginRequiredMixin, View):

    def get(self, request):
        owner = request.user
        user_plan = MyPlan.objects.filter(owner=owner)
        return render(request, 'show_plan.html', {'user_plan': user_plan})


class AllWorkouts(LoginRequiredMixin, View):

    def get(self, request):
        all_workouts = Workout.objects.all()
        return render(request, 'show_workouts.html', {'all_workouts': all_workouts})


class AllWarmups(LoginRequiredMixin, View):

    def get(self, request):
        all_warmups = WarmupExercises.objects.all()
        return render(request, 'show_warmups.html', {'all_warmups': all_warmups})


class AllStretchings(LoginRequiredMixin, View):

    def get(self, request):
        all_stretch = Stretching.objects.all()
        return render(request, 'show_stretch.html', {'all_stretch': all_stretch})


class ShowExercisesDetails_Workout(LoginRequiredMixin, View):

    def get(self, request, train_id):
        workout = Workout.objects.get(pk=train_id)
        exercises = workout.exercises.all()
        calories = 0
        for exercise in exercises:
            calories += exercise.burned_calories
        return render(request, 'details.html', {'exercises': exercises, 'calories': calories, 'workout': workout})


class ShowExercisesDetails_Warmup(LoginRequiredMixin, View):

    def get(self, request, train_id):
        warmup = WarmupExercises.objects.get(pk=train_id)
        exercises = warmup.exercises.all()
        calories = 0
        for exercise in exercises:
            calories += exercise.burned_calories
        return render(request, 'details.html', {'exercises': exercises, 'calories': calories, 'warmup': warmup})


class ShowExercisesDetails_Stretch(LoginRequiredMixin, View):

    def get(self, request, train_id):
        stretch = Stretching.objects.get(pk=train_id)
        exercises = stretch.exercises.all()
        calories = 0
        for exercise in exercises:
            calories += exercise.burned_calories
        return render(request, 'details.html', {'exercises': exercises, 'calories': calories, 'stretch': stretch})


class MyPlanDetails(LoginRequiredMixin, View):

    def get(self, request, planed_id):
        chosen_plan = MyPlan.objects.get(pk=planed_id)
        workouts = WorkoutInPlan.objects.filter(plan=chosen_plan)
        stretchings = StretchingInPlan.objects.filter(plan=chosen_plan)

        trainings = []
        for workout in workouts:
            trainings.append(workout)
        for stretching in stretchings:
            trainings.append(stretching)

        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        saturday = []
        sunday = []

        for train in trainings:
            if train.day == 1:
                monday.append(train)
            elif train.day == 2:
                tuesday.append(train)
            elif train.day == 3:
                wednesday.append(train)
            elif train.day == 4:
                thursday.append(train)
            elif train.day == 5:
                friday.append(train)
            elif train.day == 6:
                saturday.append(train)
            else:
                sunday.append(train)

        return render(request, 'plan_details.html', {
            'workouts': workouts,
            'stretchings': stretchings,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'plan': chosen_plan

        })


class DeletePlan(LoginRequiredMixin, View):

    def get(self, request, plan_id):
        p = MyPlan.objects.get(pk=plan_id)
        p.delete()
        return redirect('show_user_plan')


class DeleteWarmup(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, warmup_id):
        w = WarmupExercises.objects.get(pk=warmup_id)
        w.delete()
        return redirect('show_all_warmups')


class DeleteWorkout(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, workout_id):
        w = Workout.objects.get(pk=workout_id)
        w.delete()
        return redirect('show_all_workouts')


class DeleteStretching(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, stretch_id):
        s = Stretching.objects.get(pk=stretch_id)
        s.delete()
        return redirect('show_all_stretch')


class CreateWarmUp(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = CreateWarmUpForm()
        return render(request, 'form.html', {'form': form, 'info': 'Create new Warm up'})

    def post(self, request):
        form = CreateWarmUpForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            WarmupExercises.objects.create(title=title, description=description)
            return render(request, 'form.html', {'warmup_created': f'Warmup created'})
        return render(request, 'form.html', {'message': 'Incorrect data'})


class AddExercise_toWarmup(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, warmup_id):
        form = AddExercisesToWarmupForm()
        return render(request, 'form.html', {'form': form, 'info': 'Choose exercise and add'})

    def post(self, request, warmup_id):
        warmUp = WarmupExercises.objects.get(id=warmup_id)
        form = AddExercisesToWarmupForm(request.POST)
        if form.is_valid():
            we = form.save(commit=False)
            we.warmup = warmUp
            we.save()
            return render(request, 'form.html', {'exercises_added_1': 'Exercise added', 'warmup': warmUp})
        return render(request, 'form.html', {'message': 'Incorrect data'})


class CreateWorkout(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = CreateWorkoutForm()
        return render(request, 'form.html', {'form': form, 'info': 'Create new Workout'})

    def post(self, request):
        form = CreateWorkoutForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            intensity = form.cleaned_data['intensity']
            warmup = form.cleaned_data['warmup']
            Workout.objects.create(title=title, description=description, intensity=intensity, warmup=warmup)
            return render(request, 'form.html', {'workout_created': 'Workout created'})
        return render(request, 'form.html', {'message': 'Incorrect data'})


class AddExercise_toWorkout(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, workout_id):
        form = AddExercisesToWorkoutForm()
        return render(request, 'form.html', {'form': form, 'info': 'Choose exercise and add'})

    def post(self, request, workout_id):
        workout = Workout.objects.get(id=workout_id)
        form = AddExercisesToWorkoutForm(request.POST)
        if form.is_valid():
            we = form.save(commit=False)
            we.workout = workout
            we.save()
            return render(request, 'form.html', {'exercises_added_2': 'Exercise added', 'workout': workout})
        return render(request, 'form.html', {'message': 'Incorrect data'})


class CreateStretching(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = CreateStretchForm()
        return render(request, 'form.html', {'form': form, 'info': 'Create new stretching'})

    def post(self, request):
        form = CreateStretchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            Stretching.objects.create(title=title, description=description)
            return render(request, 'form.html', {'stretch_created': 'Stretching created'})
        return render(request, 'form.html', {'message': 'Incorrect data'})


class AddExercise_toStretching(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, stretch_id):
        form = AddExercisesToStretchForm()
        return render(request, 'form.html', {'form': form, 'info': 'Choose exercise and add'})

    def post(self, request, stretch_id):
        stretch = Stretching.objects.get(id=stretch_id)
        form = AddExercisesToStretchForm(request.POST)
        if form.is_valid():
            se = form.save(commit=False)
            se.stretching = stretch
            se.save()
            return render(request, 'form.html', {'exercises_added_3': 'Exercise added', 'stretch': stretch})
        return render(request, 'form.html', {'message': 'Incorrect data'})
