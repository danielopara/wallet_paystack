from django.urls import include, path

urlpatterns = [
    path('wallet/', include('api.wallet.urls')),
    path('auth/', include('api.auth.urls'))
]
