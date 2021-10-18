from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    city = models.CharField(
        max_length=100, null=True, blank=True, unique=False, help_text="Ex. Aranjuez"
    )
    postal_code = models.CharField(
        max_length=100, null=True, blank=True, unique=False, help_text="Ex. 28000"
    )
    state = models.CharField(
        max_length=100, null=True, blank=True, unique=False, help_text="Ex. Madrid"
    )
    public_username = models.CharField(
        max_length=150, null=True, blank=True, unique=False, help_text="Ex. nickname"
    )
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_account.username} - {self.id}'

    class Meta:
        abstract = True


class ClientAccount(Account):
    name = models.CharField(max_length=50, unique=False, help_text="Ex. John")
    surname = models.CharField(max_length=100, unique=False, help_text="Ex. Doe")


class Wallet(models.Model):
    """
    * Docs
    ** DecimalField limit: MySQL has more limitations than PostgreSQL.
    Because of that we set mysql as limitation.
    https://dev.mysql.com/doc/refman/8.0/en/precision-math-decimal-characteristics.html
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.DecimalField(max_digits=65, decimal_places=2, default=0, unique=False,
                                  editable=False, help_text="Total ammount of money in this wallet")
    date_created = models.DateTimeField(auto_now_add=True, unique=False)
    last_update = models.DateTimeField(auto_now=True, unique=False)

    class Meta:
        abstract = True


class ClientWallet(Wallet):
    """
    Client account is the only required field, the other will be filled from transactions.
    """
    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client_account.user_account.username} - {self.id}'


class WalletTransaction(models.Model):
    """
    This model is used to save a transactions registry for a wallet and change this wallet
    balance (amount of money) depending on the transaction amount.

    amount and client_wallet_account are the only required fields.
    """
    class Type(models.TextChoices):
        ERROR = 0
        TESTING = 1
        DEPOSIT = 2
        WITHDRAW = 3
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    description = models.CharField(max_length=250, null=True, blank=True, unique=False,
                                   help_text="Transaction description")
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    done = models.BooleanField(default=True, help_text="It check if the transaction was completed")
    transaction_type = models.IntegerField(
        choices=Type.choices, default=Type.TESTING.value, help_text="Add or substract money"
    )
    error_msg = models.CharField(max_length=250, null=True, blank=True, unique=False,
                                 help_text="Ex. Transaction error: negative balance")
    extra_info = models.TextField(
        null=True, blank=True, unique=False, help_text="Extra info about this transaction"
    )
    date_created = models.DateTimeField(auto_now_add=True, unique=False)
    client_wallet_account = models.ForeignKey(ClientWallet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client_wallet_account.client_account.user_account.username} - {self.id}'

    class Meta:
        abstract = True


class ClientWalletTransaction(WalletTransaction):

    def __str__(self):
        return "%s" % (self.client_wallet_account.__str__())
