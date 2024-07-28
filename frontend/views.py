from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from api import models


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
        pass


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            # User is logged in, send them to homepage
            return redirect('frontend:home')
        else:
            return render(request, 'frontend/login.html', context={})

    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            # User is logged in, send them to homepage
            return redirect('frontend:home')
        else:
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
