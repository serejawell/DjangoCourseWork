from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.functions import user_reset_password, toggle_user_status, email_verification
from users.views import RegisterView, CustomLoginView, ProfileView, ProfileUpdateView, \
 UserListView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('my_profile/', ProfileView.as_view(), name='profile'),
    path('my_profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password-reset/', user_reset_password, name='password_reset'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('toggle_status/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
]
