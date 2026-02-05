"""
URL configuration for finance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views as api_views

urlpatterns = [
    path('', api_views.index, name='home'),
    path('index.html', api_views.index, name='index_html'),
    path('expense-tracker.html', api_views.expense_tracker, name='expense_tracker_html'),
    path('dashboard.html', api_views.dashboard, name='dashboard_html'),
    path('accounts.html', api_views.accounts_page, name='accounts_html'),
    path('transactions.html', api_views.transactions_page, name='transactions_html'),
    path('features.html', api_views.features, name='features_html'),
    path('support.html', api_views.support, name='support_html'),
    path('auth.html', api_views.auth_page, name='auth_html'),
    path('support1.html', api_views.support1, name='support1_html'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]