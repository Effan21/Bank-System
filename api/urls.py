from django.urls import include, path
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'agents', views.AgentViewSet)
router.register(r'agences', views.AgenceViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'comptes', views.CompteViewSet)
router.register(r'cartes_credit', views.Carte_creditViewSet)
router.register(r'chequiers', views.ChequierViewSet)
router.register(r'beneficiaires', views.BeneficiaireViewSet)
router.register(r'virements', views.VirementViewSet)
router.register(r'operations', views.OperationsViewSet)
router.register(r'payements', views.PayementViewSet)
router.register(r'demandes_cartes', views.Demandes_cartesViewSet)
router.register(r'demandes_chequiers', views.Demandes_chequiersViewSet)
router.register(r'demandes_ouvertures_comptes', views.Demandes_ouvertures_comptesViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'FCM_Token', views.FCM_TokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path("time_based/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
]