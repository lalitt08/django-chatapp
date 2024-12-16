from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model, login
import jwt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import SignupForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Homepage view
def index(request):
    return render(request, 'index.html', {})


# Login page view
def login_u(request):
    return render(request, 'login.html', {})


# Retrieve the user model
User = get_user_model()


# Signup view
def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User needs to activate the account
            user.save()

            # Prepare the activation email
            message = render_to_string('acc_email.html', {
                'user': user,
                'domain': 'http://13.232.251.134/',  # Replace with your domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Updated to avoid `.decode()`
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate Your ChatApp Account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponse('The confirmation link has been sent to your email address.\n'
                                'Please click on the link to confirm your registration.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# Account activation view
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Updated to use `force_str`
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponsePermanentRedirect(reverse('sign_in'))
    else:
        return HttpResponse('Activation link is invalid!')


# JWT-based login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Generate JWT token
                payload = {'username': username, 'password': password}
                jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}

                print(jwt_token)
                return render(request, 'chat.html', {})
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login details provided.")
    else:
        return render(request, 'login.html', {})
