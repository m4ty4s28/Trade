from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Fees_mode(models.TextChoices):

    A = "A", "Mode_A"
    B = "B", "Mode_B"

class Usuarios(User):

    fees_mode = models.CharField(
        max_length=1,
        choices=Fees_mode.choices,
        default=Fees_mode.A
    )

class Datos(models.Model):
    
    id_transaccion = models.UUIDField(editable=False, null=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=10)
    dinero = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    fees_total = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    fees_pendiente = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    fees_cobrado = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)

    def __str__(self):
        return f"{self.usuario.username} - {self.symbol}"

class FiatPayment(Datos):

    class Meta:
        verbose_name = "FiatPayment"
        verbose_name_plural = "FiatPayments"

class Trade(Datos):

    class Meta:
        verbose_name = "Trade"
        verbose_name_plural = "Trades"

class BlockchainPayment(Datos):

    class Meta:
        verbose_name = "BlockchainPayment"
        verbose_name_plural = "BlockchainPayments"

class Logs(Datos):

    error = models.BooleanField(default=False)
    error_detail = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Logs"
        verbose_name_plural = "Logs"

class Configuracion(models.Model):
    fees = models.TextField()

    def __str__(self):
        return "Configuracion"

    class Meta:
        verbose_name = "Configuracion"
        verbose_name_plural = "Configuraciones"