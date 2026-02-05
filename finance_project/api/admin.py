from django.contrib import admin
from .models import Account, Transaction, StockPortfolio, Stock

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'user', 'account_type', 'balance')
    list_filter = ('account_type', 'user')
    search_fields = ('account_name', 'user__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'amount', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date', 'user')
    search_fields = ('description', 'user__username')

@admin.register(StockPortfolio)
class StockPortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_investment', 'current_value', 'total_gain_loss')
    search_fields = ('user__username',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'company_name', 'quantity', 'purchase_price', 'current_price', 'gain_loss')
    list_filter = ('sector', 'portfolio__user')
    search_fields = ('symbol', 'company_name')
