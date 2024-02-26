from django.contrib import admin

from .models import *

campos = ["usuario", "fecha", "symbol", "dinero", "fees_total", "fees_pendiente", "fees_cobrado", "id_transaccion"]

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ["username", "fees_mode"]

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    readonly_fields = ["id_transaccion",]
    list_display = campos
    
@admin.register(FiatPayment)
class FiatPaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["id_transaccion",]
    list_display = campos

@admin.register(BlockchainPayment)
class BlockchainPaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["id_transaccion",]
    list_display = campos

@admin.register(Logs)
class BlockchainPaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["id_transaccion",]
    list_display = campos + ["error"]

admin.site.register(Configuracion)