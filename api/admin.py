from django.contrib import admin
from .models import ClientWalletTransaction, BussinesWalletTransaction
from .models import BussinesAccount, BussinesWallet
from .models import ClientAccount, ClientWallet


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientAccount._meta.fields]


@admin.register(BussinesAccount)
class BussinesAccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BussinesAccount._meta.fields]


@admin.register(ClientWallet)
class ClientWalletAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientWallet._meta.fields]
    readonly_fields = ("balance", "last_update")


@admin.register(BussinesWallet)
class BussinesWalletAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BussinesWallet._meta.fields]
    readonly_fields = ("balance", "last_update")


@admin.register(ClientWalletTransaction)
class ClientMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClientWalletTransaction._meta.fields]


@admin.register(BussinesWalletTransaction)
class BussinesMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BussinesWalletTransaction._meta.fields]
