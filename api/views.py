from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
from twilio.rest import Client as TwilioClient
# Create your views here.

TWILIO_ACCOUNT_SID = 'AC0b998a9f24e4e8f6f62211fbd916c518'
TWILIO_AUTH_TOKEN = '24c08dd2786e8c27467d682563874773'
TWILIO_PHONE_NUMBER = '+13613373177'

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class AgenceViewSet(viewsets.ModelViewSet):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

class Carte_creditViewSet(viewsets.ModelViewSet):
    queryset = Carte_credit.objects.all()
    serializer_class = Carte_creditSerializer

class ChequierViewSet(viewsets.ModelViewSet):
    queryset = Chequier.objects.all()
    serializer_class = ChequierSerializer

class TranscationViewSet(viewsets.ModelViewSet):
    queryset = Transcation.objects.all()
    serializer_class = TranscationSerializer

class BeneficiaireViewSet(viewsets.ModelViewSet):
    queryset = Beneficiaire.objects.all()
    serializer_class = BeneficiaireSerializer

class VirementViewSet(viewsets.ModelViewSet):
    queryset = Virement.objects.all()
    serializer_class = VirementSerializer

class RechargementViewSet(viewsets.ModelViewSet):
    queryset = Rechargement.objects.all()
    serializer_class = RechargementSerializer

class PayementViewSet(viewsets.ModelViewSet):
    queryset = Payement.objects.all()
    serializer_class = PayementSerializer

class RetraitViewSet(viewsets.ModelViewSet):
    queryset = Retrait.objects.all()
    serializer_class = RetraitSerializer

class DemandesViewSet(viewsets.ModelViewSet):
    queryset = Demandes.objects.all()
    serializer_class = DemandesSerializer

class Demandes_cartesViewSet(viewsets.ModelViewSet):
    queryset = Demandes_cartes.objects.all()
    serializer_class = Demandes_cartesSerializer

class Demandes_chequiersViewSet(viewsets.ModelViewSet):
    queryset = Demandes_chequiers.objects.all()
    serializer_class = Demandes_chequiersSerializer

class Demandes_ouvertures_comptesViewSet(viewsets.ModelViewSet):
    queryset = Demandes_ouvertures_comptes.objects.all()
    serializer_class = Demandes_ouvertures_comptesSerializer

class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
        body=f"Your OTP is: {OTP.at(Mobile.counter)}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    
        print(message.sid)
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)


# Time after which OTP will expire
EXPIRY_TIME = 50 # seconds

class getPhoneNumberRegistered_TimeBased(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
        print(OTP.now())
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio
        client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
        body=f"Your OTP is: {OTP.now()}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    
        print(message.sid)

        return Response({"OTP": OTP.now()}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model 
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong/expired", status=400)