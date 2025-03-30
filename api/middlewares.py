from api.models import Wallet
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()
        auth_result = auth.authenticate(request)

        if auth_result is None:
            request.user_profile = None
            return

        user, _ = auth_result

        try:
            profile = Wallet.objects.get(user=user)
            request.wallet_profile = profile  # Attach profile to request
        except Wallet.DoesNotExist:
            return JsonResponse({"message": "User profile not found"}, status=404)
