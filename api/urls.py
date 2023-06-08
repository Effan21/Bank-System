from django.urls import include, path
from rest_framework import routers
from . import views
from .views import getPhoneNumberRegistered, getPhoneNumberRegistered_TimeBased

router = routers.DefaultRouter()
router.register(r'agents', views.AgentViewSet)
router.register(r'agences', views.AgenceViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'comptes', views.CompteViewSet)
router.register(r'cartes_credit', views.Carte_creditViewSet)
router.register(r'chequiers', views.ChequierViewSet)
router.register(r'transcations', views.TranscationViewSet)
router.register(r'beneficiaires', views.BeneficiaireViewSet)
router.register(r'virements', views.VirementViewSet)
router.register(r'rechargements', views.RechargementViewSet)
router.register(r'payements', views.PayementViewSet)
router.register(r'retraits', views.RetraitViewSet)
router.register(r'demandes', views.DemandesViewSet)
router.register(r'demandes_cartes', views.Demandes_cartesViewSet)
router.register(r'demandes_chequiers', views.Demandes_chequiersViewSet)
router.register(r'demandes_ouvertures_comptes', views.Demandes_ouvertures_comptesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path("time_based/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),
]