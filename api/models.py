import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Wallet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_wallet",
        to_field='username',
        db_column='user_username'
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=50, default='NGN')
    
    
    def __str__(self):
        return self.user.email
    
    
class Wallet_Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('transfer', 'transfer'),
        ('withdraw', 'withdraw')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    reference = models.CharField(unique=True, max_length=100)
    status = models.CharField(default='pending', max_length=20)
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.wallet.user.email} - {self.transaction_type} - {self.amount}"