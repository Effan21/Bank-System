
from django.urls import path, re_path
from bankAgent import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('comptes', views.comptes, name='comptes'),
    path('demandes_ouverture', views.demandes_ouverture, name='demandes_ouverture'),
    path('demandes_client', views.demandes_client, name='demandes_client'),
    path('cartes', views.cartes, name='cartes'),
    path('faqs', views.faqs, name='faqs'),
    path('conversations', views.conversations, name='conversations'),
    path('faq/add_faq', views.add_faq, name='add_faq'),
    path('faq/<int:faq_id>/edit_faq', views.edit_faq, name='edit_faq'),
    path('faq/<int:faq_id>/delete_faq', views.delete_faq, name='delete_faq'),
    path('cartes/<int:carte_id>/suspend', views.suspend_carte, name='suspend_carte'),
    path('cartes/<int:carte_id>/activate', views.activate_carte, name='activate_carte'),
    path('demandes_client/<int:demande_id>/accept_demande_carte', views.accept_demande_cartes, name='accept_demande_carte'),
    path('demandes_client/<int:demande_id>/reject_demande_carte', views.refuse_demande_cartes, name='reject_demande_carte'),
    path('demandes_client/<int:demande_id>/accept_demande_chequier', views.accept_demande_chequiers, name='accept_demande_chequier'),
    path('demandes_client/<int:demande_id>/reject_demande_chequier', views.refuse_demande_chequiers, name='reject_demande_chequier'),
    path('comptes/suspend/<int:compte_id>/', views.suspend_account, name='suspend_account'),
    path('comptes/activate/<int:compte_id>/', views.activate_account, name='activate_account'),
    path('clients/suspend/<int:client_id>/', views.suspend_client, name='suspend_client'),
    path('clients/activate/<int:client_id>/', views.activate_client, name='activate_client'),
    path('show_demande/<int:demande_id>/', views.show_demande, name='show_demande'),
    path('show_demande/<int:demande_id>/accept/', views.accept_demande, name='accept_demande'),
    path('show_demande/<int:demande_id>/refuse/', views.refuse_demande, name='refuse_demande'),

    # Matches any html file
    re_path(r'^.*   \.*', views.pages, name='pages'),

]
