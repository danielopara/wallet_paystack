import hashlib
import hmac
import os
import traceback
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
    paystack_key = os.getenv("PAYSTACK_KEY", settings.PAYSTACK_KEY)

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
            user = request.wallet_profile
            if not user:
                return Response({'message': 'no auth'}, status=status.HTTP_401_UNAUTHORIZED)
            
            amount = request.data.get('amount')
            
            if amount <= 0:
                return Response({'message': 'amount cannot be less or equal to 0'}, status = status.HTTP_400_BAD_REQUEST)
            
            
            headers = {
                "Authorization": f"Bearer {self.paystack_key}",
                "Content-type": 'application/json'
            }
            payload ={
                'email': user.user.email,
                'amount': int(float(amount) * 100),
            }
            
            user2 = User.objects.get(email=user)
            
            wallet = Wallet.objects.get(user=user2)
            
            response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
            res_data = response.json()
         

            if res_data.get("status") is True:
                
                reference =  res_data['data']['reference']
                
                transaction = Wallet_Transaction.objects.create(
                    wallet = wallet,
                    amount = amount,
                    transaction_type = "deposit",
                    status = "pending",
                    reference = reference,
                )
                
                serializer = WalletTransactionSerializer(transaction) 
                
                return Response({
                    "payment_url": res_data["data"]["authorization_url"],
                    "reference": res_data['data']['reference'],
                    "transaction": serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Paystack payment failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e: 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def verify_payment(self, request):
        try:
            reference = request.GET.get('reference')
            user = request.wallet_profile
            
            if not user:
                return Response({'message': 'no auth'}, status=status.HTTP_401_UNAUTHORIZED)
            user2 = User.objects.get(email=user)
            
            wallet = Wallet.objects.get(user=user2)
            transaction = Wallet_Transaction.objects.get(reference=reference)
            
            headers = {
                "Authorization": f"Bearer {self.paystack_key}",
                "Content-type": 'application/json'
            }
            
            url = f"https://api.paystack.co/transaction/verify/{reference}"
            response = requests.get(url, headers=headers)
            verification_data = response.json()
            
            if verification_data['data']['status'] == "success":
                
                wallet.balance += transaction.amount
                transaction.status = "success"
                wallet.save()
                transaction.save()
                
                serializer = WalletSerializer(wallet)
                transaction_serializer = WalletTransactionSerializer(transaction)
                return Response({'message': 'true', 'wallet_data': serializer.data, 'transaction_data': transaction_serializer.data})
            
            return Response({'data': verification_data})
        except Exception as e:
            error_trace = traceback.format_exc() 
            print(error_trace) 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
## work on webhook
    def webhook(self, request):
        try:
            paystack_signature = request.headers.get("x-paystack-signature")
            computed_signature = hmac.new(
                bytes(self.paystack_key, 'utf-8'),
                msg=request.body,
                digestmod=hashlib.sha512
            ).hexdigest()
            
            if paystack_signature != computed_signature:
                return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)
            
            payload = request.data
            event = payload.get('event')
            
            if event == 'charge.success':
                reference = payload['data']['reference']
                customer_email = payload['data']['customer']['email']
                transaction = Wallet_Transaction.objects.get(reference = reference)
                
                if transaction is not None:
                    if transaction.status == 'success':
                        print("no update")
                    transaction.status = 'success'
                    amount = transaction.amount
                    
                    user = User.objects.get(email=customer_email)
                    wallet = Wallet.objects.get(user = user)
                    
                    wallet.balance += amount
                    
                    transaction.save()
                    wallet.save()
                    print(f'payment with reference {reference} is successful')

            return Response({'data': payload})
        except Exception as e:
            error_trace = traceback.format_exc() 
            print(error_trace) 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)