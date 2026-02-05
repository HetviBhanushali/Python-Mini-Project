from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('checking', 'Checking Account'),
        ('credit', 'Credit Account'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.account_name} - {self.user.username}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('food', 'Food'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('transport', 'Transport'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.description} - {self.amount} ({self.user.username})"
    
    class Meta:
        ordering = ['-date']


class StockPortfolio(models.Model):
    """Stock portfolio for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stock_portfolio')
    total_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Portfolio - {self.user.username}"
    
    @property
    def total_gain_loss(self):
        return self.current_value - self.total_investment


class Stock(models.Model):
    """Individual stock holdings"""
    portfolio = models.ForeignKey(StockPortfolio, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.CharField(max_length=50, blank=True)
    purchase_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}"
    
    @property
    def total_cost(self):
        return self.quantity * self.purchase_price
    
    @property
    def current_value(self):
        return self.quantity * self.current_price
    
    @property
    def gain_loss(self):
        return self.current_value - self.total_cost
    
    @property
    def gain_loss_percentage(self):
        if self.total_cost == 0:
            return 0
        return (self.gain_loss / self.total_cost) * 100
