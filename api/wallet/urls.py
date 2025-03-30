from api.wallet.views import create_transaction, create_wallet
from django.urls import path

urlpatterns = [
    path('create-wallet', create_wallet),
    path('create-transaction', create_transaction)
]
