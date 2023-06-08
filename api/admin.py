from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Agent)
admin.site.register(Agence)
admin.site.register(Client)
admin.site.register(Compte)
admin.site.register(Carte_credit)
admin.site.register(Chequier)
admin.site.register(Transcation)
admin.site.register(Beneficiaire)
admin.site.register(Virement)
admin.site.register(Rechargement)
admin.site.register(Payement)
admin.site.register(Retrait)
admin.site.register(Demandes)
admin.site.register(Demandes_cartes)
admin.site.register(Demandes_chequiers)
admin.site.register(Demandes_ouvertures_comptes)
admin.site.register(phoneModel)