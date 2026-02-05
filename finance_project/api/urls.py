from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts_page, name='accounts_page'),
    path('transactions/', views.transactions_page, name='transactions_page'),
    path('stock-market/', views.stock_market, name='stock_market'),
    path('api/transactions/', views.get_transactions, name='get_transactions'),
    path('api/accounts/', views.get_accounts, name='get_accounts'),
    path('auth/', views.auth_page, name='auth_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('support1/', views.support1, name='support1'),
    path('features/', views.features, name='features'),
    path('support/', views.support, name='support'),
    path('expense-tracker/', views.expense_tracker, name='expense_tracker'),
]