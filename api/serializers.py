from api.models import Wallet, Wallet_Transaction
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'user', 'balance', 'currency')
        
        
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet_Transaction
        fields = ('id', 'wallet', 'amount', 'transaction_type', 'status', 'reference', 'created_at',)