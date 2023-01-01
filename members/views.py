from django.shortcuts import render, redirect

from members.forms import RegisterForm
from members.models import Member


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = Member.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
                username=username,
            )
            user.save()
            return redirect('login')
    else:
         form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'members/register.html', context=context)


def login(request):
    return render(request, 'members/login.html')


def logout(request):
    return
