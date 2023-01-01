from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
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
            messages.success(request, 'Account was created for ' + username)
            return redirect('register')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'members/register.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # user = Member.objects.get(email=email)
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        # if user:
        #     if user.password == password:
        #         return redirect('home')
    return render(request, 'members/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')
