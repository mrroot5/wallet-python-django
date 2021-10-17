from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    city = models.CharField(max_length=100, null=True, blank=True, unique=False, help_text="Ex. Aranjuez")
    postal_code = models.CharField(max_length=100, null=True, blank=True, unique=False, help_text="Ex. 28000")
    state = models.CharField(max_length=100, null=True, blank=True, unique=False, help_text="Ex. Madrid")
    public_username = models.CharField(max_length=150, null=True, blank=True, unique=False, help_text="Ex. nickname")
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.user_account.username

    class Meta:
        abstract = True


class ClientAccount(Account):
    name = models.CharField(max_length=50, unique=False, help_text="Ex. John")
    surname = models.CharField(max_length=100, unique=False, help_text="Ex. Doe")


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.FloatField(default=0, unique=False, editable=False,
                                help_text="Total ammount of money in this wallet")
    date_created = models.DateTimeField(auto_now_add=True, unique=False)
    last_update = models.DateTimeField(auto_now=True, unique=False)

    class Meta:
        abstract = True


class ClientWallet(Wallet):
    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.client_account.__str__())  # self.balance, "{}".format(self.id)[-5:]


class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        ERROR = 0
        TESTING = 1
        DEPOSIT = 2
        WITHDRAW = 3
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    description = models.CharField(max_length=250, null=True, blank=True, unique=False,
                                   help_text="Transaction description")
    amount = models.FloatField()
    done = models.BooleanField(default=True, help_text="It check if the transaction was completed")
    transaction_type = models.IntegerField(choices=Type.choices, default=Type.TESTING, help_text="Add or substract money")
    error_msg = models.CharField(max_length=250, null=True, blank=True, unique=False,
                                 help_text="Ex. Transaction error: negative balance ")
    extra_info = models.TextField(null=True, blank=True, unique=False, help_text="Extra info about this transaction")
    date_created = models.DateTimeField(auto_now_add=True, unique=False)
    client_wallet_account = models.ForeignKey(ClientWallet, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.user_account.username

    class Meta:
        abstract = True


class ClientWalletTransaction(WalletTransaction):
    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.client_wallet_account.__str__())
