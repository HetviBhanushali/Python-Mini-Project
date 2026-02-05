from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Account, Transaction, StockPortfolio, Stock
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime, timedelta


def get_current_user(request):
    """Get the current authenticated user or return the first user for demo purposes."""
    if request.user.is_authenticated:
        return request.user
    # For demo, return the first user
    return User.objects.first()


@require_http_methods(["GET"]) 
def get_transactions(request):
    user = get_current_user(request)
    if not user:
        return JsonResponse({"transactions": []})
    
    transactions = Transaction.objects.filter(user=user).values(
        'id', 'description', 'amount', 'category', 'transaction_type', 'date'
    )
    transactions_list = [
        {
            **trans,
            'amount': float(trans['amount']),
            'date': trans['date'].isoformat()
        }
        for trans in transactions
    ]
    return JsonResponse({"transactions": transactions_list})


@require_http_methods(["GET"]) 
def get_accounts(request):
    user = get_current_user(request)
    if not user:
        return JsonResponse({"accounts": []})
    
    accounts = Account.objects.filter(user=user).values(
        'id', 'account_name', 'account_type', 'balance', 'interest_rate', 'credit_limit'
    )
    accounts_list = [
        {
            **acc,
            'balance': float(acc['balance']),
            'interest_rate': float(acc['interest_rate']) if acc['interest_rate'] else None,
            'credit_limit': float(acc['credit_limit']) if acc['credit_limit'] else None
        }
        for acc in accounts
    ]
    return JsonResponse({"accounts": accounts_list})


def dashboard(request):
    """Display dashboard with accounts, transactions, and charts."""
    user = get_current_user(request)
    if not user:
        return redirect('index')
    
    accounts = Account.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-date')[:10]
    
    # Calculate total balance
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or Decimal('0')
    
    # Get expense totals by category
    category_totals = {}
    for trans in Transaction.objects.filter(user=user, transaction_type='expense'):
        if trans.category not in category_totals:
            category_totals[trans.category] = Decimal('0')
        category_totals[trans.category] += trans.amount
    
    # Get all transactions for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_transactions = Transaction.objects.filter(
        user=user, date__gte=thirty_days_ago
    ).order_by('-date')
    
    context = {
        'user': user,
        'accounts': accounts,
        'transactions': transactions,
        'total_balance': float(total_balance),
        'category_totals': {k: float(v) for k, v in category_totals.items()},
        'recent_transactions': recent_transactions,
    }
    return render(request, 'api/dashboard.html', context)


def index(request):
    """Home page."""
    return render(request, 'api/index.html')


def accounts_page(request):
    """Show user accounts."""
    user = get_current_user(request)
    if not user:
        return redirect('index')
    
    accounts = Account.objects.filter(user=user)
    context = {
        'user': user,
        'accounts': accounts,
    }
    return render(request, 'api/accounts.html', context)


def transactions_page(request):
    """Show user transactions."""
    user = get_current_user(request)
    if not user:
        return redirect('index')
    
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    context = {
        'user': user,
        'transactions': transactions,
    }
    return render(request, 'api/transactions.html', context)


def expense_tracker(request):
    """Expense tracker page."""
    return render(request, 'api/expense-tracker.html')


def support1(request):
    """Support page."""
    return render(request, 'api/support1.html', {})


def features(request):
    """Features page."""
    return render(request, 'api/features.html')


def support(request):
    """Support page."""
    return render(request, 'api/support.html')


@ensure_csrf_cookie
def auth_page(request):
    """Authentication page."""
    return render(request, 'api/auth.html')


@require_http_methods(["POST"])
def login_view(request):
    """Handle user login."""
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if not email or not password:
        return redirect('auth_page')

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('dashboard')
    except User.DoesNotExist:
        pass
    
    return redirect('auth_page')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('index')


def stock_market(request):
    """Display stock market analysis."""
    user = get_current_user(request)
    if not user:
        return redirect('index')

    try:
        portfolio = StockPortfolio.objects.get(user=user)
        stocks = Stock.objects.filter(portfolio=portfolio)
    except StockPortfolio.DoesNotExist:
        portfolio = None
        stocks = Stock.objects.none()

    # Portfolio stats
    total_investment = Decimal('0')
    current_value = Decimal('0')
    total_gain_loss = Decimal('0')
    sector_data = {}

    for stock in stocks:
        total_investment += stock.total_cost
        current_value += stock.current_value
        total_gain_loss += stock.gain_loss

        if stock.sector not in sector_data:
            sector_data[stock.sector] = Decimal('0')
        sector_data[stock.sector] += stock.current_value

    gain_loss_percentage = (
        (total_gain_loss / total_investment) * 100
        if total_investment > 0 else 0
    )

    context = {
        "user": user,
        "portfolio": portfolio,
        "stocks": stocks,  # ✅ QuerySet
        "total_investment": total_investment,
        "current_value": current_value,
        "total_gain_loss": total_gain_loss,
        "gain_loss_percentage": gain_loss_percentage,
        "sector_data": sector_data,  # ✅ Python dict
    }

    return render(request, "api/stock_market.html", context)
