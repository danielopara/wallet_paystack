from api.models import Wallet
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()

        
        try:
            auth_result = auth.authenticate(request)
            if auth_result is not None:
                user, _ = auth_result
                try:
                    profile = Wallet.objects.get(user=user)
                    request.wallet_profile = profile
                except Wallet.DoesNotExist:
                    request.wallet_profile = None
            else:
                request.wallet_profile = None
        except (InvalidToken, AuthenticationFailed):
            # Just mark as unauthenticated instead of returning response
            request.wallet_profile = None
            
        # Important: don't return a response here
        return None