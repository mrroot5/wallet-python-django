from django.contrib import admin
from .models import ClientWalletTransaction
from .models import ClientAccount, ClientWallet


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientAccount._meta.fields]


@admin.register(ClientWallet)
class ClientWalletAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientWallet._meta.fields]
    readonly_fields = ("balance", "last_update")


@admin.register(ClientWalletTransaction)
class ClientMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientWalletTransaction._meta.fields]
