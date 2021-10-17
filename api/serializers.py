from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import empty

from .models import ClientAccount, ClientWallet, ClientWalletTransaction
from commons.utils import RequestTools


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ("pk", "username", "first_name", "last_name", "email", "password")
        read_only_fields = ("pk",)


class BussinesAccountSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user
            validated_data["user_account"] = user
        return super(BussinesAccountSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user
            validated_data["user_account"] = user
        return super(BussinesAccountSerializer, self).update(instance, validated_data)

    class Meta:
        model = BussinesAccount
        fields = "__all__"
        read_only_fields = ("pk",)


class ClientAccountSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user
            validated_data["user_account"] = user
        return super(ClientAccountSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user
            validated_data["user_account"] = user
        return super(ClientAccountSerializer, self).update(instance, validated_data)

    class Meta:
        model = ClientAccount
        fields = "__all__"
        read_only_fields = ("pk",)


class ClientWalletSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user.pk
            client = ClientAccount.objects.get(user_account=user)
            validated_data["client_account"] = client
        return super(ClientWalletSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if RequestTools.check_if_request_user_exist(self.context):
            user = self.context.get("request").user.pk
            client = ClientAccount.objects.get(user_account=user)
            validated_data["client_account"] = client
        return super(ClientWalletSerializer, self).update(instance, validated_data)

    class Meta:
        model = ClientWallet
        fields = "__all__"
        read_only_fields = ("pk",)


class ClientWalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWalletTransaction
        fields = "__all__"
        read_only_fields = ("pk", "date_created",)
