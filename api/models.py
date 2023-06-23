from django.db import models
from django.contrib.auth.hashers import make_password



# Create your models here.
class Agent(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_naissance = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nom}"
    
class Agence(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.IntegerField()
    adresse = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom}"
    
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=14, unique=True)
    adresse = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_naissance = models.DateField()
    code_secret = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom}"
    
    
class Compte(models.Model):
    numero = models.CharField(max_length=100)
    IBAN = models.CharField(max_length=100)
    solde = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.IBAN}"
    
class Carte_credit(models.Model):
    type = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    date_expiration = models.CharField(max_length=8)
    cvv = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.numero}"

class Chequier(models.Model):
    num_page = models.IntegerField()
    date_expiration = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.num_page}"
    

class Beneficiaire(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=14, unique=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}"

class Virement(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    compte_beneficiaire = models.ForeignKey('Compte',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}"

class Operations(models.Model):
    type = models.IntegerField(choices=((0, 'Retrait'), (1, 'Dépôt')))
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    operateur = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.date}"
    
class Payement(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10)
    num_facture = models.IntegerField()
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.date}"
    

class Demandes_cartes(models.Model):

    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    )
    type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='en_attente')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}"

class Demandes_chequiers(models.Model):

    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    )

    type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='en_attente')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}"
    
class Demandes_ouvertures_comptes(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    )

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='en_attente')
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=14, unique=True)
    date_naissance = models.DateField(blank=True)
    document_pic = models.ImageField(upload_to='passport_pic')
    photo = models.ImageField(upload_to='photo', blank=True)
    signature_pic = models.ImageField(upload_to='signature', blank=True)
    adresse = models.CharField(max_length=100, blank=True)
    code_secret = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.nom)

class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)
    
    def __str__(self):
        return str(self.Mobile)
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    

class Conversation(models.Model):
    admin = models.ForeignKey(Agent, on_delete=models.CASCADE)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='conversations')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    type = models.IntegerField(choices=((0, 'Client'), (1, 'Agent')))    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class FCM_Token(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    
