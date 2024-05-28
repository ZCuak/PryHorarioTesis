from django.urls import path
from App import views
from django.contrib.auth import views as auth_views
from .views import jurados_list, jurados_create, jurados_update, jurados_delete, jurados_import


urlpatterns = [
    path('', views.index, name='index'),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('accounts/profile/', views.profile, name='profile'),
    path('jurados/listar', jurados_list, name='jurados_list'),
    path('jurados/create/', jurados_create, name='jurados_create'),
    path('jurados/update/<int:pk>/', jurados_update, name='jurados_update'),
    path('jurados/delete/<int:pk>/', jurados_delete, name='jurados_delete'),
    path('jurados/import/', jurados_import, name='jurados_import'),
    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
