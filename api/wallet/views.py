from api.wallet.service import WalletService
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_wallet(request):
    return WalletService().create_wallet(request)

@api_view(['POST'])
def create_transaction(request):
    return WalletService().create_transaction(request)