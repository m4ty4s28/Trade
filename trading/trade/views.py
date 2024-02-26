from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from django.db.models import Sum

from django.utils import timezone
from datetime import datetime

import uuid, calendar, yaml

def load_configuration():
    configuracion = Configuracion.objects.first()
    confi = yaml.safe_load(configuracion.fees)
    return confi
    
def descontar_fees(dinero, FEES):
    dinero -= dinero * FEES
    return round(float(dinero),2)

def fees_por_dinero(dinero, FEES):
    return FEES * dinero 

def get_start_end_month():
    datetime_now = timezone.now()
    year = datetime_now.year
    month = datetime_now.month
    last_day_month = calendar.monthrange(year, month)[1]
    start_month = datetime(year, month, 1)
    end_month = datetime(year, month, last_day_month, 23, 59)
    return start_month, end_month

def round_decimal(user_month_fees):
    for i,j in user_month_fees.items():
        if j != None:
            user_month_fees[i] = round(j,2)
    return user_month_fees

class TradeApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Endpoint que nos diga lo que se le ha cobrado este mes al usuario ya, y lo que está pendiente por ser cobrado.
        '''

        username = request.GET.get("username")

        try:
            Usuarios.objects.get(username=username)
        except Usuarios.DoesNotExist:
            return Response({"error" : "el usuario no existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_month, end_month = get_start_end_month()

        user_month_fees = Logs.objects.filter(
            usuario__username=username,
            fecha__gte=start_month,
            fecha__lte=end_month
            ).aggregate(
                fees_total=Sum("fees_total"),
                fees_pendiente=Sum("fees_pendiente"),
                fees_cobrado=Sum("fees_cobrado"),
                )

        user_month_fees = round_decimal(user_month_fees)

        return Response(user_month_fees, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Endpoint que me permita crear el FiatPayment y ejecute hasta el final del pago saliente.
        '''

        user = request.user
        id_transaccion = uuid.uuid4()
        usuario = Usuarios.objects.get(username=user.username)
        symbol_fiat = request.data.get("symbol_fiat")
        symbol_blockchain = request.data.get("symbol_blockchain")

        try:
            dinero = request.data.get("dinero")
            dinero = round(float(dinero),2)
        except Exception as e:
            return Response({"error" : "el dinero debe ser un numero"}, status=status.HTTP_400_BAD_REQUEST)

        if dinero <= 0:
            return Response({"error" : "el dinero debe ser un numero Positivo"}, status=status.HTTP_400_BAD_REQUEST)
        
        confi = load_configuration()
        FEES = confi.get("FEES")

        fees_mode = usuario.fees_mode
        fees_total = 0.0
        fees_pendiente = 0.0
        fees_cobrado = 0.0

        symbol = f"{symbol_fiat}/{symbol_blockchain}"

        try:
            if fees_mode == Fees_mode.A:

                fiatpayment = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol_fiat,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                FiatPayment.objects.create(**fiatpayment)

                dinero = descontar_fees(dinero, FEES)
                fees_total += fees_por_dinero(dinero, FEES)
                fees_cobrado = fees_total

                trade = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                Trade.objects.create(**trade)

                dinero = descontar_fees(dinero, FEES)
                fees_total += fees_por_dinero(dinero, FEES)
                fees_cobrado = fees_total

                blockchain = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol_blockchain,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                BlockchainPayment.objects.create(**blockchain)

                dinero = descontar_fees(dinero, FEES)
                fees_total += fees_por_dinero(dinero, FEES)
                fees_cobrado = fees_total
                
            elif fees_mode == Fees_mode.B:

                fiatpayment = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol_fiat,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                FiatPayment.objects.create(**fiatpayment)

                fees_total += fees_por_dinero(dinero, FEES)
                fees_pendiente += fees_por_dinero(dinero, FEES)

                trade = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                Trade.objects.create(**trade)

                dinero = descontar_fees(dinero, FEES)
                fees_total += fees_por_dinero(dinero, FEES)
                fees_cobrado += fees_por_dinero(dinero, FEES)

                blockchain = {
                "id_transaccion" : id_transaccion,
                "usuario" : usuario,
                "dinero" : dinero,
                "symbol" : symbol_blockchain,
                "fees_total" : fees_total,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado
                }
                BlockchainPayment.objects.create(**blockchain)

                fees_total += fees_por_dinero(dinero, FEES)
                fees_pendiente += fees_por_dinero(dinero, FEES)

            response = {
                "symbol" : symbol_blockchain,
                "dinero" : dinero,
                "fees_pendiente" : fees_pendiente,
                "fees_cobrado" : fees_cobrado,
                "fees_total" : fees_total,
                }

            logs = {
            "id_transaccion" : id_transaccion,
            "usuario" : usuario,
            "dinero" : dinero,
            "symbol" : symbol,
            "fees_total" : fees_total,
            "fees_pendiente" : fees_pendiente,
            "fees_cobrado" : fees_cobrado,
            }
            Logs.objects.create(**logs)

        except Exception as e:
            print(e)

            logs = {
            "id_transaccion" : id_transaccion,
            "usuario" : usuario,
            "dinero" : dinero,
            "symbol" : symbol,
            "fees_total" : fees_total,
            "fees_pendiente" : fees_pendiente,
            "fees_cobrado" : fees_cobrado,
            "error" : True,
            "error_detail" : str(e)
            }
            Logs.objects.create(**logs)

            return Response({"status": "KO"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(response, status=status.HTTP_201_CREATED)

