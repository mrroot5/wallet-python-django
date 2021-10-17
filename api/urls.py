from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import ClientAccountViewSet
from .views import GetNumClientAccounts
from .views import ClientWalletTransactionSet
from .views import ClientWalletViewSet
from .views import GetCurrentClientId
from .views import GetCurrentUserId
from .views import GetCurrentUserUsername
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename="user_api")
router.register(r'client', ClientAccountViewSet, basename="client_api")
router.register(r'client_wallet', ClientWalletViewSet, basename="client_wallet_api")
router.register(r'client_wallet_transaction', ClientWalletTransactionSet, basename="client_wallet_transaction_api")

urlpatterns = [
    path('', include((router.urls, "api"))),
    path('get_username/', GetCurrentUserUsername.as_view(), name="get_username"),
    path('get_user_id/', GetCurrentUserId.as_view(), name="get_user_id"),
    path('get_client_id/', GetCurrentClientId.as_view(), name="get_client_id"),
    path('get_num_accounts/', GetNumClientAccounts.as_view(), name="get_client_id"),
]
