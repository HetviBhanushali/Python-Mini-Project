from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/', views.get_transactions, name='transactions'),
    path('page/transactions/', views.transactions_page, name='transactions_page'),
    path('page/support1/', views.support1, name='support1_page'),
    path('auth/', views.auth_page, name='auth'),
    path('login/', views.login_view, name='login'),
    path('login', views.login_view, name='login_noslash'),
    path('logout/', views.logout_view, name='logout'),
    path('logout', views.logout_view, name='logout_noslash'),
]