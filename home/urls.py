from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('archive/', views.archive, name="archive"),
    path('update-session/', views.update_session_variable, name='update_session_variable'),
]

    