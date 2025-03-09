from django.shortcuts import redirect
from django.contrib import messages
from .models import Community, CommunityUser
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured


class PermissionRequiredMixin:
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing the permission_required attribute. Define %(cls)s.permission_required, or override "
                "%(cls)s.dispatch()." % {
                    'cls': self.__class__.__name__
                }
            )

        # Retrieve community identifier from request data
        community_identifier = request.data.get('community_slug') #or request.data.get('community_id')

        if not community_identifier:
            raise PermissionDenied("Community identifier is missing.")

        try:
            community = Community.objects.get(slug__iexact=community_identifier) #or Community.objects.get(pk=community_identifier)
            community_user = CommunityUser.objects.get(user=request.user, community=community)
            role = community_user.role

            if role.permissions.filter(name=self.permission_required).exists():
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied("You do not have the required permission.")

        except Community.DoesNotExist:
            raise PermissionDenied("Community not found.")
        except CommunityUser.DoesNotExist:
            raise PermissionDenied("You do not have permission to access this community.")
