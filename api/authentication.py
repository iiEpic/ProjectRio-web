from rest_framework import authentication

from api.models import Token


class TokenAuthentication(authentication.TokenAuthentication):
    model = Token
