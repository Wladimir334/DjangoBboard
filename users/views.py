from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from BboardSite.settings import LOGIN_REDIRECT_URL
from django.contrib.auth import update_session_auth_hash
from BboardSite.settings import LOGIN_REDIRECT_URL
from .forms import NewRegistrationForm, CustomPasswordChangeForm
                    # UserRegistrationForm, ChangePasswordForm)

User = get_user_model()
def register(request):
    if request.method == "POST":
        form = NewRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            context = {"title": "Регистрация завершена", "new_user": new_user}
            return render(request, template_name="users/registration_done.html", context=context)

    form = NewRegistrationForm()
    context = {"title": "Регистрация пользователя", "register_form": form}
    return render(request, template_name="users/registration.html", context=context)

def log_in(request):
    # создание формы аутентификации
    form = AuthenticationForm(request, request.POST)
    # проверка формы
    if form.is_valid():
        # получение логина и пароля из формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # аутентификация пользователя (проверка наличия поль-ля и пароля)
        user = authenticate(username=username, password=password)
        if user:
            # авторизация пользователя (получение прав доступа)
            login(request, user)
            # получение дальнейшего маршрута после авторизации (next - путь, откуда пришел пользователь)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)


@login_required
def log_out(request):
    logout(request)
    return redirect('blog:index')


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
       raise PermissionDenied()

    context = {'user': user, 'title': 'Информация о профиле'}
    return render(request, template_name='users/profile.html', context=context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            if not request.user.check_password(old_password):
                messages.error(request, "Старый пароль не верный")
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Ваш пароль успешно изменен")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, template_name="users/change_password.html", context={"form": form})

