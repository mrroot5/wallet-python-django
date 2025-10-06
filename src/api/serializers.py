from typing import Optional

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import serializers
from rest_framework.fields import empty

from .models import ClientAccount, ClientWallet, ClientWalletTransaction


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Used to generate a password with django algorithm
        """
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ("pk", "username", "first_name", "last_name", "email", "password", "is_staff")
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ("pk",)


class ClientAccountSerializer(serializers.ModelSerializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        request = self.context.get('request')

        if request and request.user.is_staff:
            self.Meta.exclude = ()
        else:
            self.Meta.exclude = ('user_account',)

    def create(self, validated_data):
        if not validated_data.get('user_account'):
            try:
                validated_data["user_account"] = self.context.get("request").user
            except (TypeError, AttributeError):
                pass
        return super(ClientAccountSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(ClientAccountSerializer, self).update(instance, validated_data)

    class Meta:
        model = ClientAccount
        exclude = ('user_account',)
        read_only_fields = ("id",)


class ClientWalletSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        This method only allows to create a wallet if user is_staff or
        if it is his own account.
        """
        try:
            user: Optional[User] = self.context.get("request").user
        except (TypeError, AttributeError):
            user = None
        if user and not user.is_staff:
            try:
                if user.clientaccount.id != validated_data.get('client_account').id:
                    raise Http404
            except (TypeError, AttributeError):
                raise Http404
        return super().create(validated_data)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data) \
                if self.context.get("request").user.is_superuser else Http404
        except (TypeError, AttributeError):
            raise Http404

    class Meta:
        model = ClientWallet
        fields = "__all__"
        read_only_fields = ("pk",)


class ClientWalletTransactionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        This method only allows to create a transaction if user is_staff or
        if it is his own wallet.
        """
        try:
            user: Optional[User] = self.context.get("request").user
        except (TypeError, AttributeError):
            user = None
        if user and not user.is_staff:
            try:
                user.clientaccount.clientwallet_set.get(
                    id=validated_data.get('client_wallet_account').id
                )
            except ClientWallet.DoesNotExist:
                raise Http404
        return super().create(validated_data)

    class Meta:
        model = ClientWalletTransaction
        fields = "__all__"
        read_only_fields = ("pk", "date_created", "transaction_type", "done")
