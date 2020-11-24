from django.urls import path 
from . import views

app_name='login'
urlpatterns = [
    path('', views.home),
    path('app', views.index,name='index'),
    path('login', views.login_form,name='login_link'),
    path('accounts/login/', views.login_redirect_form),
    path('logout',views.logout_view,name='logout')
]