from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
# from BboardSite.settings import LOGIN_REDIRECT_URL
from .forms import NewRegistrationForm
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


# @login_required
# def change_password(request):
#     if request.method == "POST":
#         is_valid = True
#         form = CustomPasswordChangeForm(request.POST)
#
#         if form.is_valid():
#             old_password = form.cleaned_data['old_password']
#             new_password = form.cleaned_data['new_password_1']
#
#             if request.user.check_password(old_password):
#                 if form.cleaned_data['new_password_1'] != form.cleaned_data['new_password_2']:
#                     form.add_error('new_password_1', 'Пароли не совпадают')
#                     is_valid = False
#
#                 if not is_valid:
#                     return render(request, template_name='users/change_password.html', context={'form': form})
#
#                 request.user.set_password(new_password)
#                 request.user.save()
#                 update_session_auth_hash(request, request.user)
#
#             else:
#                 form.add_error('old_password', 'Старый пароль неверный')
#                 render(request, template_name='users/change_password.html', context={'form': form})
#
#         context = {'form': form}
#         return render(request, template_name='users/change_password.html', context=context)
#
#     else:
#         form = CustomPasswordChangeForm()
#         context = {'title': 'Сменить пароль', 'form': form}
#         return render(request, template_name='users/change_password.html', context=context)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            # Проверка правильности старого пароля
            if not request.user.check_password(old_password):
                form.add_error('old_password', 'Старый пароль неверен.')
            else:
                # Изменение пароля
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Сохраняем сессию пользователя
                messages.success(request, 'Пароль успешно изменен.')
                return redirect('some_view')  # Замените на нужный вам URL

    else:
        form = ChangePasswordForm()

    return render(request, 'users/change_password.html', {'form': form})