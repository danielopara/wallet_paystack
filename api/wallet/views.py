from api.wallet.service import WalletService
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def create_wallet(request):
    return WalletService().create_wallet(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    return WalletService().create_transaction(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    return WalletService().verify_payment(request)