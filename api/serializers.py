from typing import Optional

from django.contrib.auth.models import User
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
        if self.context.get('request').user.is_staff:
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
        try:
            user: Optional[int] = self.context.get("request").user.pk
        except (TypeError, AttributeError):
            user = None
        if user:
            client = ClientAccount.objects.get(user_account=user)
            validated_data["client_account"] = client
        return super().create(validated_data)

    def update(self, instance, validated_data):
        try:
            user: Optional[int] = self.context.get("request").user.pk
        except (TypeError, AttributeError):
            user = None
        if user:
            client = ClientAccount.objects.get(user_account=user)
            validated_data["client_account"] = client
        return super().update(instance, validated_data)

    class Meta:
        model = ClientWallet
        fields = "__all__"
        read_only_fields = ("pk",)


class ClientWalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWalletTransaction
        fields = "__all__"
        read_only_fields = ("pk", "date_created",)
