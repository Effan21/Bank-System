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
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
import random
from rest_framework.decorators import api_view
import json
from rest_framework import generics


# Create your views here.

TWILIO_ACCOUNT_SID = 'AC0b998a9f24e4e8f6f62211fbd916c518'
TWILIO_AUTH_TOKEN = '00fd42e493029585b707551ba4fd0d9d'
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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    
class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['client']
    lookup_field = 'client'
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.solde = request.data.get('solde')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class Carte_creditViewSet(viewsets.ModelViewSet):
    queryset = Carte_credit.objects.all()
    serializer_class = Carte_creditSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['compte']   

class ChequierViewSet(viewsets.ModelViewSet):
    queryset = Chequier.objects.all()
    serializer_class = ChequierSerializer


class BeneficiaireViewSet(viewsets.ModelViewSet):
    queryset = Beneficiaire.objects.all()
    serializer_class = BeneficiaireSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['client']   

class VirementViewSet(viewsets.ModelViewSet):
    queryset = Virement.objects.all()
    serializer_class = VirementSerializer

class OperationsViewSet(viewsets.ModelViewSet):
    queryset = Operations.objects.all()
    serializer_class = OperationsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['compte']   

class PayementViewSet(viewsets.ModelViewSet):
    queryset = Payement.objects.all()
    serializer_class = PayementSerializer


class Demandes_cartesViewSet(viewsets.ModelViewSet):
    queryset = Demandes_cartes.objects.all()
    serializer_class = Demandes_cartesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['client']   

class Demandes_chequiersViewSet(viewsets.ModelViewSet):
    queryset = Demandes_chequiers.objects.all()
    serializer_class = Demandes_chequiersSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['client']   

class Demandes_ouvertures_comptesViewSet(viewsets.ModelViewSet):
    queryset = Demandes_ouvertures_comptes.objects.all()
    serializer_class = Demandes_ouvertures_comptesSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user']

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class FCM_TokenViewSet(viewsets.ModelViewSet):
    queryset = FCM_Token.objects.all()
    serializer_class = FCM_TokenSerializer


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
        otp = request.GET.get('otp')

        if OTP.verify(otp, Mobile.counter):  # Verifying the OTP
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
    

class GenerateCreditCardView(APIView):
    @staticmethod
    def get():
        # Generate a random credit card number
        credit_card_number = ''.join(random.choice('0123456789') for _ in range(16))

        # Generate a random CVV code (3 digits)
        cvv_code = ''.join(random.choice('0123456789') for _ in range(3))

        # Generate a random expiry date (between 01/2023 and 12/2030)
        expiry_month = random.randint(1, 12)
        expiry_year = random.randint(2023, 2030)

        # Construct the JSON response
        response_data = {
            'credit_card_number': credit_card_number,
            'cvv_code': cvv_code,
            'expiry_date': f'{expiry_month:02d}/{expiry_year}'
        }

        return Response(response_data)
