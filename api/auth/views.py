from api.auth.service import AuthService
from rest_framework.decorators import api_view


@api_view(['POST'])
def login(request):
    return AuthService().login(request)