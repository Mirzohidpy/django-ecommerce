from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('members/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            send_email.send()
            # messages.success(request, 'Account was created for ' + username)
            return redirect('members/login/?command=verification&email=' + email)
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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Member._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully')
        # auth.login(request, user)
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

