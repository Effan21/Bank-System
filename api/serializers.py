from rest_framework import serializers
from .models import *

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CompteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Compte
        fields = '__all__'      

class Carte_creditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carte_credit
        fields = '__all__'

class ChequierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chequier
        fields = '__all__'

class TranscationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcation
        fields = '__all__'

class BeneficiaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaire
        fields = '__all__'

class VirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Virement
        fields = '__all__'

class RechargementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rechargement
        fields = '__all__'

class PayementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement
        fields = '__all__'

class RetraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retrait
        fields = '__all__'

class DemandesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandes
        fields = '__all__'

class Demandes_cartesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandes_cartes
        fields = '__all__'

class Demandes_chequiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandes_chequiers
        fields = '__all__'

class Demandes_ouvertures_comptesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandes_ouvertures_comptes
        fields = '__all__'

