from django.db import models
from django.contrib.auth.hashers import make_password
from django_cryptography.fields import encrypt

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
    contact = models.IntegerField(max_length=10)
    adresse = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom}"
    
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.IntegerField(max_length=10)
    adresse = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_naissance = models.DateField()
    code_secret = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=100, unique=True, blank=True)
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.code_secret = make_password(self.password)
        super().save(*args, **kwargs)
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
        return f"{self.numero}"
    
class Carte_credit(models.Model):
    type = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    date_expiration = models.DateField()
    cvv = models.IntegerField(max_length=3)
    date_creation = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cvv = encrypt(self.cvv)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero}"

class Chequier(models.Model):
    num_page = models.IntegerField(max_length=3)
    date_expiration = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.numero}"
    
class Transcation(models.Model):
    type = models.CharField(max_length=100)
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.type}"
    
class Beneficiaire(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.IntegerField(max_length=10)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}"

class Virement(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    beneficiaire = models.ForeignKey('Beneficiaire', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.montant}"

class Rechargement(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    operateur = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.montant}"
    
class Payement(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)
    num_facture = models.IntegerField(max_length=10)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)
    
    

    def __str__(self):
        return f"{self.montant}"
    
class Retrait(models.Model):
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    operateur = models.CharField(max_length=30)
    compte = models.ForeignKey('Compte', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.montant}"
    
class Demandes(models.Model):
    type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}"

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
    contact = models.IntegerField(max_length=10, unique=True)
    document_pic = models.ImageField(upload_to='passport_pic')
    photo = models.ImageField(upload_to='photo')

    def __str__(self):
        return str(self.nom)

class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)
    
    def __str__(self):
        return str(self.Mobile)