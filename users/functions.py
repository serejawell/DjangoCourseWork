import random
import string
from email import message

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from config import settings
from newsletter.models import Newsletter
from users.forms import PasswordResetForm
from users.models import User

def email_verification(request, token):
    '''Фукнция верификации через отправку сообщения на почту'''
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

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



def toggle_user_status(request, user_id):
    '''Функция блокировки/разблокировки пользователя'''
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active  # Меняем статус
    user.save()
    return redirect('users:user_list')  # Возвращаемся к списку пользователей

def toggle_newsletter_status(request, newsletter_id):
    '''Функция переключения статуса рассылки между "Запущена" и "Остановлена"'''
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    # Меняем статус
    newsletter.status = 'stopped' if newsletter.status == 'started' else 'started'
    newsletter.save()
    return redirect('newsletter:newsletter_list_all')  # Возвращаемся к списку рассылок