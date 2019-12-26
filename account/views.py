from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .decarators.decorator import anonymous_required
from account.forms import LoginForm, RegisterForm


@anonymous_required
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username =form.cleaned_data.get('username')
        password =form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('mainPage'))
    context = {'form': form}
    return render(request, 'account/auth.html', context=context)

@anonymous_required
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        messages.success(request, "Aramıza xoş gəldin", extra_tags="success")
        return HttpResponseRedirect(reverse('mainPage'))
    context = {'form': form}
    return render(request, 'account/register.html', context=context)

@login_required()
def password_change_view(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Şifrə yeniləndi", extra_tags="success")
            return HttpResponseRedirect(reverse('mainPage'))
    context = {'form': form}
    return render(request, 'account/password.html', context=context)

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("loginView"))