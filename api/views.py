from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from .serializers import BussinesAccountSerializer, BussinesWalletSerializer
from .serializers import ClientAccountSerializer, ClientWalletSerializer
from .serializers import BussinesWalletTransactionSerializer
from .serializers import ClientWalletTransactionSerializer
from .models import BussinesAccount, BussinesWallet, BussinesWalletTransaction
from .models import ClientAccount, ClientWallet, ClientWalletTransaction
from .serializers import UserSerializer
from django.db import transaction


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user.pk
        return User.objects.filter(user_account=user.pk)


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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@authentication_classes((authentication.SessionAuthentication, authentication.BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def get_current_user_username(request):
    json_response = {"username": request.user.username}
    return Response(json_response)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@authentication_classes((authentication.SessionAuthentication, authentication.BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def get_current_user_id(request):
    json_response = {"id": request.user.pk}
    return Response(json_response)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@authentication_classes((authentication.SessionAuthentication, authentication.BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def get_current_client_id(request):
    client = ClientAccount.objects.get(user_fk=request.user.pk)
    json_response = {"id": client.id}
    return Response(json_response)
