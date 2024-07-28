from api import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect, reverse
from django.views import View
from frontend.forms import LoginForm, RegisterForm


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'frontend/home.html', context={})


class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            # User is logged in, send them to homepage
            return redirect('frontend:home')
        else:
            return render(request, 'frontend/register.html', context={})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            # Check if there is a user with that username already
            if User.objects.filter(username__iexact=username).first() is not None:
                messages.add_message(request, messages.ERROR, "User already exists with that name.", extra_tags='danger')

            # Check if there is a user with that email already
            if User.objects.filter(email__iexact=email).first() is not None:
                messages.add_message(request, messages.ERROR, "User already exists with that email.", extra_tags='danger')

            # Check if password is valid
            try:
                validate_password(password1)
            except:
                messages.add_message(request, messages.ERROR, "Password does not match criteria stated.", extra_tags='danger')

            # Check if passwords match one another
            if password1 != password2:
                messages.add_message(request, messages.ERROR, "Passwords does not match.", extra_tags='danger')

            if len(messages.get_messages(request)) > 0:
                return render(request, 'frontend/register.html', context={})

            # We passed all the checks, create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            rio_user = models.RioUser.objects.create(
                user=user,
            )

            user = authenticate(request, username=username, password=password1)
            login(request, user)
            # User is logged in, send them to homepage
            return redirect('frontend:home')
        messages.add_message(request, messages.ERROR, "Form was invalid. Try again", extra_tags='danger')
        return render(request, 'frontend/register.html', context={})


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            # User is logged in, send them to homepage
            return redirect('frontend:home')
        else:
            return render(request, 'frontend/login.html', context={})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # User is logged in, send them to homepage
                return redirect('frontend:home')
        messages.add_message(request, messages.ERROR, "Wrong username or password.", extra_tags='danger')
        return render(request, 'frontend/login.html', context={})


class Logout(View):
    def get(self, request):
        # Log the user out
        logout(request)
        # Send them to the homepage
        return redirect('frontend:home')


class Users(View):
    def get(self, request, *args, **kwargs):
        try:
            if kwargs['username'][-1] == '/':
                kwargs['username'] = kwargs['username'][:-1]
        except IndexError:
            # Chances are the kwargs is empty, continue as normal
            pass
        if kwargs['username'].lower() in ['', 'all']:
            # We are returning the entire user database that isn't marked private
            # Get all users that are not marked "Private" if the requester is NOT staff
            if not request.user.is_staff:
                user_list = models.RioUser.objects.filter(private=False)
            else:
                user_list = models.RioUser.objects.all()
            return render(request, 'frontend/all_users.html', context={'users': user_list})
        else:
            # Check if user being requested actually exists
            user_object = models.RioUser.objects.filter(user__username__iexact=kwargs['username']).first()
            if user_object is not None:
                # Found User, check if user is private and if the requester is a staff member
                if user_object.private and not request.user.is_staff:
                    # User is private, tell requester that the user does not exist
                    return render(request, 'frontend/user.html', context={'user': None,
                                                                          'username': kwargs['username']})
                return render(request, 'frontend/user.html', context={'user': user_object})
            else:
                # User does not exist
                return render(request, 'frontend/user.html', context={'user': None,
                                                                      'username': kwargs['username']})

    def post(self, request, *args, **kwargs):
        pass


class UserBatting(View):
    def get(self, request, *args, **kwargs):
        user_object = models.RioUser.objects.filter(user__username__iexact=kwargs['username']).first()
        if user_object is not None:
            # Found User
            return render(request, 'frontend/user.html', context={'user': user_object})

    def post(self, request, *args, **kwargs):
        pass


class UserPitching(View):
    def get(self, request, *args, **kwargs):
        user_object = models.RioUser.objects.filter(user__username__iexact=kwargs['username']).first()
        if user_object is not None:
            # Found User
            return render(request, 'frontend/user.html', context={'user': user_object})

    def post(self, request, *args, **kwargs):
        pass
