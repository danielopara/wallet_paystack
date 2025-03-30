import os
import uuid
from wsgiref import headers

import requests
from api.models import Wallet, Wallet_Transaction
from api.serializers import WalletSerializer, WalletTransactionSerializer
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response


class WalletService:
    def create_wallet(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            if User.objects.filter(username=username).exists():
                return Response({'message': 'username is taken'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'message': 'email exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            wallet = Wallet.objects.create(user=user)
            serializer = WalletSerializer(wallet)
            return Response({
                'message': 'wallet created',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def create_transaction(self, request):
        try:
            user = request.data.get('email')
            amount = request.data.get('amount')
            reference = str(uuid.uuid4())
            
            paystack_key = os.getenv("PAYSTACK_KEY", settings.PAYSTACK_KEY)
            
            headers = {
                "Authorization": f"Bearer {paystack_key}",
                "Content-type": 'application/json'
            }
            payload ={
                'email': user,
                'amount': amount,
            }
            
            # Wallet.objects.get(user__email=user)
            
            response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
            res_data = response.json()
         

            if res_data.get("status") is True:
                return Response({
                    "payment_url": res_data["data"]["authorization_url"],
                    "data" : res_data['data']
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Paystack payment failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)