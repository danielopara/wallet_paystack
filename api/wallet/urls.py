from api.wallet.views import create_transaction, create_wallet, verify_payment
from django.urls import path

urlpatterns = [
    path('create-wallet', create_wallet),
    path('create-transaction', create_transaction),
    path('verify-transaction', verify_payment)
]
