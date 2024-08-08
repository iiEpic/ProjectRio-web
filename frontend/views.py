from api import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect, reverse
from django.views import View
from frontend.forms import LoginForm, RegisterForm


class Communities(View):
    def get(self, request, *args, **kwargs):
        try:
            if kwargs['name'][-1] == '/':
                kwargs['name'] = kwargs['name'][:-1]
        except IndexError:
            # Chances are the kwargs is empty, continue as normal
            pass
        if kwargs['name'].lower() in ['', 'all']:
            # We are returning the entire community database that isn't marked private
            # Get all communities that are not marked "Private" if the requester is NOT staff
            if request.user.is_anonymous:
                public_list = models.Community.objects.filter(private=False)
                return render(request, 'frontend/all_items.html', context={'item_type': 'communities',
                                                                           'communities': public_list})
            if not request.user.is_staff:
                # User is not staff but try to find private communities the user is apart of
                user_object = models.RioUser.objects.filter(user=request.user).first()
                private_list = models.Community.objects.filter(communityuser__user__exact=user_object)
                public_list = models.Community.objects.filter(private=False)
                community_list = private_list | public_list
            else:
                community_list = models.Community.objects.all()
            return render(request, 'frontend/all_items.html', context={'item_type': 'communities',
                                                                       'communities': community_list})
        else:
            # Check if community being requested actually exists
            community_object = models.Community.objects.filter(name__iexact=kwargs['name']).first()
            if community_object is not None:
                # Found Community, check if community is private and if the requester is a staff member
                if community_object.private and not request.user.is_staff:
                    # Community is private, see if requester has access to it
                    if request.user.is_anonymous:
                        return render(request, 'frontend/view_community.html',
                                      context={'community': None,
                                               'community_name': kwargs['name']})
                    community_user_object = models.CommunityUser.objects.filter(
                        user=request.user,
                        community=community_object,
                        banned=False).first()
                    if community_user_object is None:
                        # User does not have access to community
                        return render(request, 'frontend/view_community.html', context={'community': None,
                                                                              'community_name': kwargs['name']})
                tag_sets = models.TagSet.objects.filter(community=community_object)
                tags = models.Tag.objects.filter(community=community_object)
                return render(request, 'frontend/view_community.html',
                              context={'community': community_object, 'tag_sets': tag_sets, 'tags': tags})
            else:
                # Community does not exist
                return render(request, 'frontend/view_community.html', context={'community': None,
                                                                           'community_name': kwargs['name']})


class Home(View):
    def get(self, request):
        return render(request, 'frontend/home.html', context={})


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


class Tags(View):
    def get(self, request, *args, **kwargs):
        try:
            if kwargs['name'][-1] == '/':
                kwargs['name'] = kwargs['name'][:-1]
        except IndexError:
            # Chances are the kwargs is empty, continue as normal
            pass
        if kwargs['name'].lower() in ['', 'all']:
            # We are returning the entire tag database
            tag_list = models.Tag.objects.all()
            return render(request, 'frontend/all_items.html', context={'item_type': 'tags',
                                                                       'tags': tag_list})
        else:
            # Check if community being requested actually exists
            tag_object = models.Tag.objects.filter(name__iexact=kwargs['name']).first()
            if tag_object is not None:
                # Found Tag, get all public tag sets that it is apart of
                tag_sets = models.TagSet.objects.filter(tags__name__iexact=tag_object.name)
                return render(request, 'frontend/view_tag.html',
                              context={'tag': tag_object, 'tag_sets': tag_sets})
            else:
                # Tag does not exist
                return render(request, 'frontend/view_tag.html',
                              context={'tag': None, 'tag_name': kwargs['name']})


class Tagsets(View):
    # TagSets are called "Gamemodes" on the front-end
    def get(self, request, *args, **kwargs):
        # Check if request has any get arguments
        if len(request.GET) != 0:
            # Key should only be type at this point
            if list(request.GET.keys())[0] == 'type':
                tag_set_list = models.TagSet.objects.filter(community__community_type__iexact=request.GET.get('type'))
                return render(request, 'frontend/all_items.html',
                              context={'item_type': 'gamemodes',
                                       'tag_sets': tag_set_list,
                                       'type': request.GET.get('type')
                                       }
                              )
        try:
            if kwargs['name'][-1] == '/':
                kwargs['name'] = kwargs['name'][:-1]
        except IndexError:
            # Chances are the kwargs is empty, continue as normal
            pass
        if kwargs['name'].lower() in ['', 'all']:
            # We are returning the entire tag database
            tag_set_list = models.TagSet.objects.all()
            return render(request, 'frontend/all_items.html', context={'item_type': 'gamemodes',
                                                                       'tag_sets': tag_set_list})
        else:
            # Check if community being requested actually exists
            tag_set_object = models.TagSet.objects.filter(name__iexact=kwargs['name']).first()
            if tag_set_object is not None:
                # Found Tagset, get community if public
                if request.user.is_authenticated:
                    user_object = models.RioUser.objects.filter(user=request.user).first()
                else:
                    return render(request, 'frontend/view_gamemode.html',
                                  context={'tag_set': tag_set_object})
                if tag_set_object.community.private and models.CommunityUser.objects.filter(
                        user=user_object, community=tag_set_object.community).first() is not None:
                    community = tag_set_object.community
                else:
                    community = None
                return render(request, 'frontend/view_gamemode.html',
                              context={'tag_set': tag_set_object, 'community': community})
            else:
                # Tag does not exist
                return render(request, 'frontend/view_gamemode.html',
                              context={'tag_set': None, 'tag_set_name': kwargs['name']})


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
