import logging
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import authentication
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.permissions import AnonCreateAndUpdateOwnerOnly, ListStaffOnly, IsStaff
from commons.utils import ClassUtils
from .models import ClientAccount, WalletTransaction
from .models import ClientWallet
from .models import ClientWalletTransaction
from .serializers import ClientAccountSerializer
from .serializers import ClientWalletSerializer
from .serializers import ClientWalletTransactionSerializer
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Anonymous users could create their own accounts.
    Only staff users could see the users list.
    Regular users could only see their own accounts
    """
    permission_classes = (AnonCreateAndUpdateOwnerOnly, ListStaffOnly,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ClientAccountViewSet(viewsets.ModelViewSet):
    """
    Regular users could only interact with their own accounts.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientAccountSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return ClientAccount.objects.all()
        return ClientAccount.objects.filter(user_account_id=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ClientWalletViewSet(viewsets.ModelViewSet):
    """
    Regular users could only interact with their own wallets.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientWalletSerializer

    def get_queryset(self):
        # client = ClientAccount.objects.get(id=self.request.user.pk)
        if self.request.user.is_staff:
            return ClientWallet.objects.all()
        return ClientWallet.objects.filter(client_account__id=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        """Only allowed for superusers"""
        if not self.request.user.is_superuser:
            raise Http404
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ClientWalletTransactionSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """
    Regular users could only interact with their own wallets.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientWalletTransactionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            ClientWalletTransaction.objects.all()
        try:
            return ClientWalletTransaction.objects.filter(
                client_wallet_account__client_account_id=self.request.user.pk
            )
        except (ClientAccount.DoesNotExist, ClientWalletTransaction.DoesNotExist):
            raise Http404

    def create(self, request, *args, **kwargs) -> Response:
        """
        * Docs
        ** Transaction atomic:
        https://docs.djangoproject.com/en/3.2/topics/db/transactions/#controlling-transactions-explicitly
        :return: A django rest framework response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet_token = request.data.get("client_wallet_account")
        amount = serializer.validated_data.get("amount", 0)
        if amount > 0:
            serializer.validated_data["transaction_type"] = ClientWalletTransaction.Type.DEPOSIT.value
        elif amount < 0:
            serializer.validated_data["transaction_type"] = ClientWalletTransaction.Type.WITHDRAW.value
        else:
            serializer.validated_data["transaction_type"] = ClientWalletTransaction.Type.TESTING.value
        with transaction.atomic():
            client_wallet = ClientWallet.objects.select_for_update().get(id=wallet_token)
            if serializer.validated_data.get('transaction_type') not in [
                WalletTransaction.Type.TESTING,
                WalletTransaction.Type.ERROR
            ]:
                client_wallet.balance += amount
            client_wallet.save()
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetCurrentUserUsername(APIView):
    """
    Sample view to see your own username in JSON format.
    """
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        json_response = {"username": request.user.username}
        return Response(json_response)


class GetCurrentUserId(APIView):
    """
    Sample view to see your own user id in JSON format.
    """
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        json_response = {"id": request.user.pk}
        return Response(json_response)


class GetCurrentClientId(APIView):
    """
    Sample view to see your own client account id in JSON format.
    """
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        client = get_object_or_404(ClientAccount, user_account=request.user.pk)
        json_response = {"id": client.id}
        return Response(json_response)


class GetNumClientAccounts(APIView):
    """
    Sample view to see users with account in JSON format.
    It uses Django Aggregation.
    """
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (IsStaff,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        users = User.objects.annotate(num_accounts=Count('clientaccount'))
        json_response = []
        allowed_data = ['id', 'username', 'num_accounts']
        for user in users:
            json_response.append(
                ClassUtils.get_class_instance_properties_as_dict(user, allowed_data)
            )
        return Response(json_response)
