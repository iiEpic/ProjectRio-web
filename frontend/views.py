from django.shortcuts import render
from django.views import View


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'home.html', context={})


class Register(View):
    def get(self, request):
        return render(request, 'register.html', context={})

    def post(self, request):
        pass

