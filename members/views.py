from django.shortcuts import render

from members.forms import RegisterForm


# Create your views here.
def register(request):
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'members/register.html', context=context)


def login(request):
    return render(request, 'members/login.html')


def logout(request):
    return
