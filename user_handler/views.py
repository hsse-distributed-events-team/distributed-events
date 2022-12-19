from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from .db_controller import *


def register(request):  # place where the user can register
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            region = form.cleaned_data.get("region")
            username = form.cleaned_data.get('username')
            django_user = get_django_user(username)
            user = create_user_for_django_user(django_user)  # НЕ ТРОГАТЬ. КОСТЫЛЬ.

            add_region_of_user(username=str(username), region=region)

            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('/login')
    else:
        form = UserRegisterForm()

    context = {'page-name': 'Мои мероприятия(участник)',
               'form': form,
               'navigation_buttons': [
                   {
                       'name': "Главная",
                       'href': ".."
                   },
                   {
                       'name': "Войти",
                       'href': "../login/"
                   }
               ]
               }

    return render(request, 'user_handler/register.html', context)


@login_required
def profile(request):  # go to profile page
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()

            username = request.user.username

            region = u_form.cleaned_data.get("region")
            email = u_form.cleaned_data.get('email')
            name = u_form.cleaned_data.get('name')
            surname = u_form.cleaned_data.get('surname')
            data = [username, email, name, surname, region]
            update_user_profile(data)

            # print(update_user_profile(data), '\n\n', username)

            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {'page-name': 'хз',
               'u_form': u_form,
               'navigation_buttons': [
                   {
                       'name': 'О нас',
                       'href': 'https://hsse.mipt.ru/'
                   },
                   {
                       'name': "Главная",
                       'href': ".."
                   },
                   {
                       'name': 'Выйти',
                       'href': '/logout'
                   },
               ]
               }

    return render(request, 'user_handler/user_profile.html', context)


def test(request):  # тест-функция. адрес: /test
    print(add_region_of_user(username=str("TEST10"), region=30))
    return HttpResponse('С кайфом')
