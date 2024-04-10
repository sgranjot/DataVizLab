from django.urls import path, include

from . import views



urlpatterns = [
    #path('login/', views.user_login, name='login'),                                                            #vista creada por nosotros

    #vistas que vienen con django
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', include('django.contrib.auth.urls')),                                                              #es lo mismo que los cuatro path anteriores
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register')
]