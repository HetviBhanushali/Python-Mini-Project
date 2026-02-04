from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os
from pathlib import Path


def load_json_data():
    """Load demo data from data.json located at the repository root."""
    # file is expected two levels up from this file: finance_project/api -> ../.. -> repo root
    base = Path(__file__).resolve().parent.parent.parent
    json_path = base / 'data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


@require_http_methods(["GET"]) 
def get_transactions(request):
    data = load_json_data()
    # return transactions for current session user if present
    user_id = request.session.get('user_id')
    if user_id:
        for u in data.get('users', []):
            if u.get('id') == user_id:
                return JsonResponse({"transactions": u.get('transactions', [])})
    return JsonResponse({"transactions": []})


@require_http_methods(["GET"]) 
def get_accounts(request):
    data = load_json_data()
    user_id = request.session.get('user_id')
    if user_id:
        for u in data.get('users', []):
            if u.get('id') == user_id:
                return JsonResponse({"accounts": u.get('accounts', [])})
    return JsonResponse({"accounts": []})


def dashboard(request):
    # require login for dashboard; redirect to auth if not logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/auth.html')
    data = load_json_data()
    user = None
    for u in data.get('users', []):
        if u.get('id') == user_id:
            user = u
            break
    return render(request, 'api/dashboard.html', {'data': user})


def index(request):
    return render(request, 'api/index.html')


def accounts(request):
    data = load_json_data()
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        for u in data.get('users', []):
            if u.get('id') == user_id:
                user = u
                break
    if user is None and data.get('users'):
        user = data['users'][0]
    return render(request, 'api/accounts.html', {'accounts': user.get('accounts', []) if user else []})


def transactions_page(request):
    data = load_json_data()
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        for u in data.get('users', []):
            if u.get('id') == user_id:
                user = u
                break
    if user is None and data.get('users'):
        user = data['users'][0]
    return render(request, 'api/transactions.html', {'transactions': user.get('transactions', []) if user else []})

def expense_tracker(request):
    # Render the static expense tracker demo page
    return render(request, 'api/expense-tracker.html')

def support1(request):
    # support page doesn't need user-specific data for this demo
    return render(request, 'api/support1.html', {})

def features(request):
    return render(request, 'api/features.html')

def support(request):
    return render(request, 'api/support.html')


@ensure_csrf_cookie
def auth_page(request):
    return render(request, 'api/auth.html')


@require_http_methods(["POST"])
def login_view(request):
    # Use normal POST form (CSRF enforced). Accept any login id/email and set session.
    data = load_json_data()
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not email:
        return redirect('/auth.html?error=Email+required')

    # Try to find a matching user in demo data; if found and has password, validate it.
    for u in data.get('users', []):
        if u.get('email') == email:
            expected = u.get('password')
            if expected is not None and (not password or password != expected):
                return redirect('/auth.html?error=Invalid+credentials')
            request.session['user_id'] = u.get('id')
            return redirect('/dashboard.html')

    # If user not found in demo data, accept the login and store the email as session id
    request.session['user_id'] = email
    return redirect('/dashboard.html')


def logout_view(request):
    request.session.pop('user_id', None)
    return JsonResponse({'ok': True})
