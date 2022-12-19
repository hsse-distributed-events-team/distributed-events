from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


def register(request):  # place where the user can register
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):   # go to profile page
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        #print(u_form)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
    name = {
        'u_form': u_form
    }

    return render(request, 'user_profile.html', name)
