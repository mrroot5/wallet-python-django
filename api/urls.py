from django.urls import path, include
from rest_framework import routers
from .views import get_current_user_username
from .views import BussinesAccountViewSet, BussinesWalletViewSet
from .views import ClientAccountViewSet, ClientWalletViewSet
from .views import ClientWalletTransactionSet, BussinesWalletTransactionSet
from .views import get_current_client_id
from .views import get_current_user_id
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename="UserViewSet")
router.register(r'client', ClientAccountViewSet, basename="ClientAccountViewSet")
router.register(r'bussines', BussinesAccountViewSet, basename="BussinesAccountViewSet")
router.register(r'client_wallet', ClientWalletViewSet, basename="ClientWalletViewSet")
router.register(r'bussines_wallet', BussinesWalletViewSet, basename="BussinesWalletViewSet")
router.register(r'client_wallet_transaction', ClientWalletTransactionSet, basename="ClientWalletTransactionSet")
router.register(r'bussines_wallet_transaction', BussinesWalletTransactionSet, basename="BussinesWalletTransactionSet")

urlpatterns = [
    path('', include(router.urls)),
    path('get_username/', get_current_user_username, name="get_username"),
    path('get_user_id/', get_current_user_id, name="get_user_id"),
    path('get_client_id/', get_current_client_id, name="get_client_id"),
]
