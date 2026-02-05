from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Account, Transaction, StockPortfolio, Stock
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample users, accounts, transactions, and stocks'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Account.objects.all().delete()
        Transaction.objects.all().delete()
        StockPortfolio.objects.all().delete()
        Stock.objects.all().delete()

        # Sample data for 3 users with stocks
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'password123',
                'accounts': [
                    {'account_type': 'savings', 'account_name': 'Emergency Fund', 'balance': Decimal('15000.00'), 'interest_rate': Decimal('4.5')},
                    {'account_type': 'checking', 'account_name': 'Daily Spending', 'balance': Decimal('3500.50'), 'interest_rate': None},
                    {'account_type': 'credit', 'account_name': 'Credit Card', 'balance': Decimal('-2100.00'), 'credit_limit': Decimal('10000.00')},
                ],
                'stocks': [
                    {'symbol': 'TCS', 'company_name': 'Tata Consultancy Services', 'quantity': 50, 'purchase_price': Decimal('2500.00'), 'current_price': Decimal('3200.00'), 'sector': 'IT'},
                    {'symbol': 'INFY', 'company_name': 'Infosys', 'quantity': 30, 'purchase_price': Decimal('1800.00'), 'current_price': Decimal('2100.00'), 'sector': 'IT'},
                    {'symbol': 'HDFC', 'company_name': 'HDFC Bank', 'quantity': 20, 'purchase_price': Decimal('1500.00'), 'current_price': Decimal('1850.00'), 'sector': 'Banking'},
                ]
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'secure456',
                'accounts': [
                    {'account_type': 'savings', 'account_name': 'Vacation Fund', 'balance': Decimal('8500.75'), 'interest_rate': Decimal('4.5')},
                    {'account_type': 'checking', 'account_name': 'Main Account', 'balance': Decimal('5200.25'), 'interest_rate': None},
                    {'account_type': 'credit', 'account_name': 'Business Credit', 'balance': Decimal('-1500.50'), 'credit_limit': Decimal('15000.00')},
                ],
                'stocks': [
                    {'symbol': 'RELIANCE', 'company_name': 'Reliance Industries', 'quantity': 40, 'purchase_price': Decimal('2000.00'), 'current_price': Decimal('2450.00'), 'sector': 'Energy'},
                    {'symbol': 'WIPRO', 'company_name': 'Wipro Limited', 'quantity': 25, 'purchase_price': Decimal('650.00'), 'current_price': Decimal('720.00'), 'sector': 'IT'},
                    {'symbol': 'BAJAJ', 'company_name': 'Bajaj Auto', 'quantity': 15, 'purchase_price': Decimal('5500.00'), 'current_price': Decimal('6200.00'), 'sector': 'Automobile'},
                ]
            },
            {
                'username': 'mike_wilson',
                'email': 'mike@example.com',
                'password': 'mikeypass',
                'accounts': [
                    {'account_type': 'savings', 'account_name': 'Retirement Plan', 'balance': Decimal('45000.00'), 'interest_rate': Decimal('5.0')},
                    {'account_type': 'checking', 'account_name': 'Work Account', 'balance': Decimal('2800.75'), 'interest_rate': None},
                    {'account_type': 'credit', 'account_name': 'Premium Card', 'balance': Decimal('-3200.00'), 'credit_limit': Decimal('20000.00')},
                ],
                'stocks': [
                    {'symbol': 'MARUTI', 'company_name': 'Maruti Suzuki', 'quantity': 35, 'purchase_price': Decimal('8000.00'), 'current_price': Decimal('9100.00'), 'sector': 'Automobile'},
                    {'symbol': 'SBIN', 'company_name': 'State Bank of India', 'quantity': 60, 'purchase_price': Decimal('500.00'), 'current_price': Decimal('580.00'), 'sector': 'Banking'},
                    {'symbol': 'SUNPHARMA', 'company_name': 'Sun Pharmaceutical', 'quantity': 45, 'purchase_price': Decimal('700.00'), 'current_price': Decimal('820.00'), 'sector': 'Pharmaceuticals'},
                ]
            },
        ]

        for user_data in users_data:
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

            # Create accounts
            accounts = []
            for account_data in user_data['accounts']:
                account = Account.objects.create(
                    user=user,
                    account_type=account_data['account_type'],
                    account_name=account_data['account_name'],
                    balance=account_data['balance'],
                    interest_rate=account_data.get('interest_rate'),
                    credit_limit=account_data.get('credit_limit'),
                )
                accounts.append(account)
                self.stdout.write(self.style.SUCCESS(f'  Created account: {account.account_name}'))

            # Create stock portfolio
            portfolio = StockPortfolio.objects.create(user=user)
            total_investment = Decimal('0')
            current_value = Decimal('0')

            # Create stocks
            for stock_data in user_data['stocks']:
                stock = Stock.objects.create(
                    portfolio=portfolio,
                    symbol=stock_data['symbol'],
                    company_name=stock_data['company_name'],
                    quantity=stock_data['quantity'],
                    purchase_price=stock_data['purchase_price'],
                    current_price=stock_data['current_price'],
                    sector=stock_data['sector'],
                )
                total_investment += stock.total_cost
                current_value += stock.current_value
                self.stdout.write(self.style.SUCCESS(f'  Created stock: {stock.symbol} ({stock.company_name})'))

            # Update portfolio totals
            portfolio.total_investment = total_investment
            portfolio.current_value = current_value
            portfolio.save()

            # Create sample transactions for each account
            categories = ['salary', 'food', 'utilities', 'entertainment', 'shopping', 'transport', 'healthcare']
            descriptions = {
                'salary': ['Monthly Salary', 'Bonus Payment', 'Freelance Income'],
                'food': ['Grocery Store', 'Restaurant', 'Coffee Shop', 'Burger King'],
                'utilities': ['Electric Bill', 'Water Bill', 'Internet Bill'],
                'entertainment': ['Movie Tickets', 'Spotify', 'Gaming', 'Concert'],
                'shopping': ['Amazon', 'Walmart', 'Target', 'Fashion Store'],
                'transport': ['Gas', 'Uber', 'Public Transport', 'Car Maintenance'],
                'healthcare': ['Pharmacy', 'Doctor Visit', 'Gym Membership'],
            }

            # Generate transactions for the last 60 days
            for account in accounts:
                num_transactions = random.randint(8, 15)
                for i in range(num_transactions):
                    category = random.choice(categories)
                    is_income = category == 'salary'
                    trans_type = 'income' if is_income else 'expense'
                    
                    if is_income:
                        amount = Decimal(random.randint(2000, 5000))
                    else:
                        amount = Decimal(random.randint(10, 500))
                    
                    description = random.choice(descriptions[category])
                    days_ago = random.randint(1, 60)
                    trans_date = datetime.now() - timedelta(days=days_ago)

                    Transaction.objects.create(
                        user=user,
                        account=account,
                        transaction_type=trans_type,
                        category=category,
                        amount=amount,
                        description=description,
                        date=trans_date,
                    )

            self.stdout.write(self.style.SUCCESS(f'  Created transactions and portfolio for {user.username}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
