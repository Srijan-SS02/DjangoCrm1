from django.urls import path

from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name="home"),
    path('users/', views.userPage, name="user-page"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>', views.customer, name='customer'),
    
    path('account/', views.accountSettings, name='account'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password_reset'),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]


