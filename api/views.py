from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BussinesAccount
from .models import BussinesWallet
from .models import BussinesWalletTransaction
from .models import ClientAccount
from .models import ClientWallet
from .models import ClientWalletTransaction
from .serializers import BussinesAccountSerializer
from .serializers import BussinesWalletSerializer
from .serializers import BussinesWalletTransactionSerializer
from .serializers import ClientAccountSerializer
from .serializers import ClientWalletSerializer
from .serializers import ClientWalletTransactionSerializer
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.pk)


class BussinesAccountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BussinesAccountSerializer

    def get_queryset(self):
        user = self.request.user.pk
        return BussinesAccount.objects.filter(user_account=user)


class ClientAccountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientAccountSerializer

    def get_queryset(self):
        user = self.request.user.pk
        return ClientAccount.objects.filter(user_account=user)


class ClientWalletViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientWalletSerializer

    def get_queryset(self):
        client = ClientAccount.objects.get(user_account=self.request.user.pk)
        return ClientWallet.objects.filter(client_account=client)


class BussinesWalletViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BussinesWalletSerializer

    def get_queryset(self):
        bussines = BussinesAccount.objects.get(user_account=self.request.user.pk)
        return BussinesWallet.objects.filter(bussines_account=bussines)


class ClientWalletTransactionSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientWalletTransactionSerializer

    def get_queryset(self):
        client = ClientAccount.objects.get(user_account=self.request.user.pk)
        return ClientWalletTransaction.objects.filter(client_account=client.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet_token = request.data.get("client_wallet_account")
        money_amount = round(float(serializer.validated_data.get("ammount")), 2)
        serializer.validated_data["ammount"] = money_amount

        with transaction.atomic():
            client_wallet = ClientWallet.objects.select_for_update().get(id=wallet_token)
            client_wallet.balance += money_amount
            client_wallet.save()
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BussinesWalletTransactionSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BussinesWalletTransactionSerializer

    def get_queryset(self):
        wallet = BussinesWallet.objects.get(
            bussines_account=BussinesAccount.objects.get(user_account=self.request.user.pk).pk)
        return BussinesWalletTransaction.objects.filter(bussines_wallet_account=wallet.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bussines_token = request.data.get("bussines_wallet_account")
        client_token = request.data.get("client_wallet_account")
        money_amount = round(float(serializer.validated_data.get("ammount")), 2)
        serializer.validated_data["ammount"] = money_amount

        with transaction.atomic():
            client_wallet = ClientWallet.objects.select_for_update().get(id=client_token)
            if client_wallet.balance < money_amount:
                serializer.validated_data["done"] = False
                serializer.validated_data["error_msg"] = "Transaction error: insufficient funds"
            else:
                client_wallet.balance -= money_amount
                client_wallet.save()
                wallet = BussinesWallet.objects.select_for_update().get(id=bussines_token)
                wallet.balance += money_amount
                wallet.save()
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetCurrentUserUsername(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        json_response = {"username": request.user.username}
        return Response(json_response)


class GetCurrentUserId(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        json_response = {"id": request.user.pk}
        return Response(json_response)


class GetCurrentClientId(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        client = ClientAccount.objects.get(user_account=request.user.pk)
        json_response = {"id": client.id}
        return Response(json_response)
