import json
import requests

from api import models
from api.forms import TagForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from frontend.forms import LoginForm, RegisterForm
from django.http import JsonResponse


class Community(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        # Check if we are creating a new TagSet
        if request.path == '/community/create/':
            return render(request, 'frontend/create_community.html', context={})

        # Check if we are looking for a specific TagSet
        if request.resolver_match.kwargs:
            community_object = models.Community.objects.filter(slug__iexact=request.resolver_match.kwargs['slug']).first()
            # Check if community_object is None, which means the community does not exist
            # Check if requested community is private, if so ensure we have proper permissions to view
            if (community_object is None or
                    (community_object.private and request.user not in [i for i in community_object.members.all()]) and
                not self.request.user.is_staff
            ):
                return render(request, 'frontend/view_community.html',
                              context={
                                  'community': None,
                                  'community_name': kwargs['slug']
                              })
            tag_sets = models.TagSet.objects.filter(community=community_object)
            tags = models.Tag.objects.filter(community=community_object)
            return render(
                request,
                'frontend/view_community.html',
                context={
                    'community': community_object,
                    'tag_sets': tag_sets,
                    'tags': tags
                }
            )

        # If we made it here, we are returning all communities that are public and the user is apart of
        # unless a user is a staff member, then return it all
        if self.request.user.is_staff:
            communities = list(models.Community.objects.all())
        else:
            communities = []
            for item in models.CommunityUser.objects.filter(user=self.request.user):
                communities.append(item.community)

            for public_community in models.Community.objects.filter(private=False):
                communities.append(public_community)

            communities = list(set(communities))

        return render(
            request,
            'frontend/all_items.html',
            context={
              'item_type': 'communities',
              'communities': communities
            }
        )

    def post(self, request, *args, **kwargs):
        data = {**request.POST}
        if 'global_link' in data.keys():
            data['global_link'] = 1 if data['global_link'][0] == 'on' else 0

        user_object = models.UserProfile.objects.get(user=request.user)
        url = request.build_absolute_uri(reverse('api:community'))
        headers = {
            'Authorization': f"Token {user_object.api_key}"
        }
        response = requests.post(url, headers=headers, data=data)

        results = json.loads(response.text)
        if results['results'] == 'error':
            return render(request, 'frontend/create_community.html', context=results)
        else:
            return redirect(reverse('frontend:communities',
                                    kwargs={'name': results['results']['community']['name']}))


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


class Tags(LoginRequiredMixin, View):

    def create(self):
        communities = models.CommunityUser.objects.filter(user=self.request.user, role__name='Admin')
        return render(self.request, 'frontend/create_tag.html', context={'communities': communities})

    def get(self, request, *args, **kwargs):

        # Check if we are creating a new TagSet
        if request.path == '/tag/create/':
            return self.create()

        # Check if we are looking for a specific TagSet
        if request.resolver_match.kwargs:
            tag_object = models.Tag.objects.filter(slug__iexact=request.resolver_match.kwargs['slug']).first()
            if tag_object is not None:
                tag_sets = list(models.TagSet.objects.filter(tags__name__iexact=tag_object.name))
                for tag_set in tag_sets.copy():
                    if models.CommunityUser.objects.filter(user=request.user, community=tag_set.community, status='active').first() is None:
                        tag_sets.remove(tag_set)
                return render(request, 'frontend/view_tag.html',
                              context={'tag': tag_object, 'tag_sets': tag_sets})

        # If we made it here, we are returning all TagSets to the user
        tag_list = models.Tag.objects.all()
        return render(
            request,
            'frontend/all_items.html',
            context={
                'item_type': 'tags',
                'tags': tag_list
                }
            )

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.cleaned_data['community'] = models.Community.objects.filter(name__iexact=form.cleaned_data.get('community_name')).first()
            form.cleaned_data.pop('community_name')
            community_user = models.CommunityUser.objects.filter(community=form.cleaned_data['community'], user=self.request.user).first()

            # The following is being checked:
            # - Community exists by the name the user gave
            # - CommunityUser exists for the community given and user trying to post
            # - CommunityUser is an admin in that Community
            # Check if the user has access to add a Tag to this community, and they didn't forge the post request
            if form.cleaned_data['community'] is None or community_user is None or community_user.role.name != 'Admin':
                form.add_error('community_name', 'Could not find a community with that name')
                communities = models.CommunityUser.objects.filter(user=self.request.user, role__name='Admin')
                return render(
                    request,
                    'frontend/create_tag.html',
                    context={'communities': communities, 'errors': form.errors}
                )

            if form.cleaned_data['gecko_code'] == '':
                form.cleaned_data.pop('gecko_code')
                form.cleaned_data.pop('gecko_code_desc')

            tag_object = models.Tag.objects.create(**form.cleaned_data)

            return redirect(reverse('frontend:tag_detail',
                                    kwargs={'slug': tag_object.slug}))


class Tagsets(LoginRequiredMixin, View):
    # TagSets are called "Gamemodes" on the front-end

    def create(self):
        return render(self.request, 'wip.html', context={})

    def get(self, request, *args, **kwargs):
        # TODO: Rework this entire thing

        # Check if we are creating a new TagSet
        if request.path == '/gamemode/create/':
            return self.create()

        # Check if we are looking for a specific TagSet
        if request.resolver_match.kwargs:
            tagset = models.TagSet.objects.filter(slug__iexact=request.resolver_match.kwargs['slug']).first()
            community_user = models.CommunityUser.objects.filter(user=request.user, community=tagset.community,
                                                                 status='active').first()
            if tagset is None or community_user is None:
                return render(request, 'frontend/view_gamemode.html',
                              context={'tag_set': None, 'tag_set_name': kwargs['slug']})

            return render(request, 'frontend/view_gamemode.html', context={'tag_set': tagset})

        # Verify if the user has the ability to view each TagSet
        community_user = models.CommunityUser.objects.filter(user=request.user)

        data = []
        for item in community_user:
            for tagset in models.TagSet.objects.filter(community=item.community):
                data.append(tagset)

        # This will get either Official or Unofficial gamemodes
        if 'type' in request.GET:
            # data = [i for i in data.filter(community__community_type__iexact=request.GET.get('type'))]
            data = [i for i in data if i.community.community_type.lower() == request.GET.get('type').lower()]

        return render(request, 'frontend/all_items.html',
                      context={'item_type': 'gamemodes',
                               'tag_sets': data,
                               'type': request.GET.get('type') if 'type' in request.GET else None
                               }
                      )


class Users(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # TODO : Rework this entire thing

        # Check if we are looking for a specific TagSet
        if request.resolver_match.kwargs:
            user_object = models.UserProfile.objects.filter(user__username__iexact=request.resolver_match.kwargs['username']).first()
            # Check if user_object is None, which means the user does not exist
            # Check if requested user is private, if so ensure we have proper permissions to view
            if user_object is None or (user_object.private and not request.user.is_staff):
                return render(request,
                              'frontend/user.html',
                              context={
                                  'user': None,
                                  'username': kwargs['username']
                              }
                              )

            return render(request, 'frontend/user.html', context={'user': user_object})

        user_objects = list(models.UserProfile.objects.all())
        if not self.request.user.is_staff:
            user_objects = [i for i in user_objects if not i.private]

        return render(request, 'frontend/all_users.html', context={'users': user_objects})


    def post(self, request, *args, **kwargs):
        pass


class UserBatting(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_object = models.RioUser.objects.filter(user__username__iexact=kwargs['username']).first()
        if user_object is not None:
            # Found User
            return render(request, 'frontend/user.html', context={'user': user_object})

    def post(self, request, *args, **kwargs):
        pass


class UserPitching(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_object = models.RioUser.objects.filter(user__username__iexact=kwargs['username']).first()
        if user_object is not None:
            # Found User
            return render(request, 'frontend/user.html', context={'user': user_object})

    def post(self, request, *args, **kwargs):
        pass
