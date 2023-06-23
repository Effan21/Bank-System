from django.shortcuts import redirect, get_object_or_404
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.template import loader
from django.urls import reverse
from api.models import *
from api.views import *
import random
import string
from BankApp import settings


def login(request):

    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']
        
        
        try:
            agent = Agent.objects.get(email=email)
        except Agent.DoesNotExist:
            return render(request, 'accounts/login.html', {'msg': 'Identifiants incorects'})
        
        if check_password(password, agent.password):
            print('password correct')
            request.session['agent_id'] = agent.id
            return redirect('home')
         
        else:
            print('password incorrect')
            
            return render(request, 'accounts/login.html', {'msg': 'Identifiants incorects'})
    
    
    
    return render(request, 'accounts/login.html')

@login_required(login_url="/login/")
def index(request):
    Virement_list = Virement.objects.all()
    Operations_list = Operations.objects.all()    
    context = {'segment': 'index'
               ,'Virement_list': Virement_list,
               'Operations_list': Operations_list}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def comptes(request):
    Compte_list = Compte.objects.all()
    Client_list = Client.objects.all()

    context = {'segment': 'comptes',
               'Compte_list': Compte_list,
               'Client_list': Client_list}

    html_template = loader.get_template('home/tables-comptes.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def demandes_ouverture(request):
    Demande_ouverture_list = Demandes_ouvertures_comptes.objects.all()
    context = {'segment': 'demandes',
               'Demande_ouverture_list': Demande_ouverture_list}

    html_template = loader.get_template('home/tables-ouv-compte.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def demandes_client(request):
    Demandes_chequiers_list = Demandes_chequiers.objects.all()
    Demandes_cartes_list = Demandes_cartes.objects.all()
    context = {'segment': 'demandes',
               'Demandes_chequiers_list': Demandes_chequiers_list,
               'Demandes_cartes_list': Demandes_cartes_list}
    
    html_template = loader.get_template('home/tables-demandes.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def accept_demande_cartes(request, demande_id):
    demande = Demandes_cartes.objects.get(id=demande_id)
    demande.status = 'Approuvée'
    demande.save()
    return redirect('demandes_client')

@login_required(login_url="/login/")
def refuse_demande_cartes(request, demande_id):
    demande = Demandes_cartes.objects.get(id=demande_id)
    demande.status = 'Rejetée'
    demande.save()
    return redirect('demandes_client')

@login_required(login_url="/login/")
def accept_demande_chequiers(request, demande_id):
    demande = Demandes_chequiers.objects.get(id=demande_id)
    demande.status = 'Approuvée'
    demande.save()
    return redirect('demandes_client')

@login_required(login_url="/login/")
def refuse_demande_chequiers(request, demande_id):
    demande = Demandes_chequiers.objects.get(id=demande_id)
    demande.status = 'Rejetée'
    demande.save()
    return redirect('demandes_client')


@login_required(login_url="/login")
def show_demande(request, demande_id):
    demandes = get_object_or_404(Demandes_ouvertures_comptes, id=demande_id)
    context = {'demandes': demandes}
    html_template = loader.get_template('home/demandes.html')
    return HttpResponse(html_template.render(context, request))

def suspend_account(request, compte_id):
    compte = get_object_or_404(Compte, pk=compte_id)
    compte.is_active = False
    compte.save()
    return redirect('comptes')  

def accept_demande(request, demande_id):
    demande = Demandes_ouvertures_comptes.objects.get(id=demande_id)

    agence = Agence.objects.get(id=2)

    client = Client.objects.create(
    nom=demande.nom,
    email=demande.email,
    contact=demande.contact,
    adresse=demande.adresse,
    date_naissance=demande.date_naissance,
    agence=agence,
    code_secret=demande.code_secret
    )

    iban = generate_iban()
    numero = generate_numero(iban)

    # Create a new compte for the client

    compte = Compte.objects.create(
    IBAN=iban,
    numero=numero,
    solde=0.0,
    client=client,
    )


    generate_credit_card_view = GenerateCreditCardView()
    response = generate_credit_card_view.get()
    credit_card_details = response.data

    # Create a new carte credit for the client
    Carte_credit.objects.create(
        type='Visa',
        numero=credit_card_details['credit_card_number'],
        date_expiration=credit_card_details['expiry_date'],
        cvv=credit_card_details['cvv_code'],
        compte=compte
    )

    demande.status = 'Approuvée'
    demande.save()

    return redirect('demandes_ouverture')

def generate_iban():
    country_code = "CI"
    iban_length = 16 - len(country_code)  # Assuming IBAN length is 16

    # Generate random alphanumeric characters for the remaining IBAN digits
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=iban_length))

    # Combine the country code and random characters to form the IBAN
    iban = country_code + random_chars

    return iban

def generate_numero(iban):
    iban_digits = ''.join(filter(str.isdigit, iban))  # Extract only the digits from the IBAN

    # Generate random numeric characters for the remaining account number digits
    remaining_digits = 12 - len(iban_digits)  # Assuming account number length is 12
    random_digits = ''.join(random.choices(string.digits, k=remaining_digits))

    # Combine the IBAN digits and random digits to form the account number
    numero = iban_digits + random_digits

    return numero

def refuse_demande(request, demande_id):
    demande = Demandes_ouvertures_comptes.objects.get(id=demande_id)
    demande.status = 'Rejetée'
    demande.save()
    return redirect('demandes_ouverture')

def activate_account(request, compte_id):
    compte = get_object_or_404(Compte, pk=compte_id)
    compte.is_active = True
    compte.save()
    return redirect('comptes')

def suspend_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.is_active = False
    client.save()
    return redirect('comptes') 

def activate_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.is_active = True
    client.save()
    return redirect('comptes')

def cartes(request):
    Carte_credit_list = Carte_credit.objects.all()
    Chequier_list = Chequier.objects.all()
    context = {'segment': 'cartes',
               'Carte_credit_list': Carte_credit_list,
               'Chequier_list': Chequier_list}

    html_template = loader.get_template('home/tables-cartes.html')
    return HttpResponse(html_template.render(context, request))

def activate_carte(request, carte_id):
    carte = get_object_or_404(Carte_credit, pk=carte_id)
    carte.is_active = True
    carte.save()
    return redirect('cartes')

def suspend_carte(request, carte_id):
    carte = get_object_or_404(Carte_credit, pk=carte_id)
    carte.is_active = False
    carte.save()
    return redirect('cartes')

def faqs(request):
    faqs_list = FAQ.objects.all()
    context = {'segment': 'faqs',
               'faqs_list': faqs_list}

    html_template = loader.get_template('home/tables-faqs.html')
    return HttpResponse(html_template.render(context, request))

def add_faq(request):
    if request.method == 'POST':
        FAQ.objects.create(
            question=request.POST['question'],
            answer=request.POST['answer']
        )
        return redirect('faqs')
    
    return render(request, 'home/add_faq.html')

    

def delete_faq(request, faq_id):
    faq = FAQ.objects.get(id=faq_id)
    faq.delete()
    return redirect('faqs')

def edit_faq(request, faq_id):
    faq = FAQ.objects.get(id=faq_id)
    if request.method == 'POST':
        faq.question = request.POST['question']
        faq.answer = request.POST['answer']
        faq.save()
        return redirect('faqs')
    
    context = {'faq': faq}
    return render(request, 'home/edit_faq.html', context)

def conversations(request):
    

    conversations_list = Conversation.objects.all()
    message_list = []
    refresh_interval = getattr(settings, 'CHAT_REFRESH_INTERVAL', 5000) 

    for conversation in conversations_list:
        conversations = conversation
        messages = Message.objects.filter(conversation=conversation)
        message_list.append({'conversation': conversation, 'messages': messages})
        
    context = {'segment': 'conversations',
               'conversations_list': conversations_list,
               'message_list': message_list,
               'conversations': conversations,
               'refresh_interval': refresh_interval}
    
    if request.method == 'POST':

        Message.objects.create(
            conversation=conversation,
            type=1,
            content=request.POST['message']
        )
        return redirect('conversations')

    html_template = loader.get_template('home/conversations.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'tables':

            html_template = loader.get_template('home/' + load_template)
            return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
