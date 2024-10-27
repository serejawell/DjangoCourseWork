import random
import secrets
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from config import settings
from users.forms import UserRegisterForm, CustomLoginForm, UserProfileForm, PasswordResetForm
from users.models import User


class RegisterView(CreateView):
    '''Форма регистрации с отправкой сообщения на почту'''
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/account/email-confirm/{token}'
        send_mail(
            subject='Welcome to the Serega Agency!',
            message=
            f'''Hello, {user.first_name} {user.last_name}!
            Thank you for registering!
            Link for confirm email: {url}''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_verification(request, token):
    '''Фукнция верификации через отправку сообщения на почту'''
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomLoginView(LoginView):
    '''Кастомный логинвью уже со стилями'''
    form_class = CustomLoginForm
    template_name = 'users/login.html'


class ProfileView(LoginRequiredMixin, DetailView):
    '''Контроллер для просмотра профиля'''
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер для обновления профиля'''
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

def generate_random_password(length=8):
    '''Функций генерирует рандомный пароль для пользователя'''
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def user_reset_password(request):
    '''Фукнция восстановления пароля пользователя через кнопку "забыл пароль"'''
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                new_password = generate_random_password()
                user.password = make_password(new_password)
                user.save()
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(f'New password: {new_password}')  # Для проверки нового пароля
                messages.success(request, 'Новый пароль отправлен на вашу почту.')

            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден.')
            except Exception as e:
                messages.error(request, f'Произошла ошибка: {str(e)}')

    # Возврат рендеринга формы вне блока if
    return render(request, 'users/password_reset.html', {'form': form})