from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Couleur (models.Model):
    nom = models.CharField(max_length=12)
    code = models.CharField(max_length=7)
    def __str__(self):
        return self.nom


class Joueur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invite = models.BooleanField(default=False)
    code = models.CharField(max_length=6, default="", blank=True)
    first = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    niveau = models.IntegerField(default=1)
    date_lastscore = models.DateTimeField(null=True, default=timezone.now)
    nb_bonnes_reponses = models.IntegerField(default=0)
    nb_reponses_donnees = models.IntegerField(default=0)

    class Meta:
        verbose_name="Pseudo"
        ordering = ['-score', 'date_lastscore']

    def __str__(self):
        return self.user.username

    def level(self):
        i,s = 1,0
        while (s+i*150<self.score):
            s = s + i * 150
            i=i+1
        return i



class Chapitre(models.Model):
    nom = models.CharField(max_length=15)
    prerequis = models.TextField(default="opérateurs numériques, opérateurs logiques, boucles")
    introduction = models.TextField(blank=True)
    couleurfond = models.ForeignKey("Couleur", on_delete=models.CASCADE)
    illustration = models.ImageField(upload_to='illustrations', blank=True)
    niveau = models.IntegerField(default=1)
    index = models.IntegerField(default=1)


    def __str__(self):
        return self.nom

class Enigme(models.Model):
    numero = models.IntegerField()
    texte = models.TextField(blank=False)
    reponse = models.IntegerField(blank=False)
    points = models.IntegerField()
    chapitre = models.ForeignKey("Chapitre", on_delete=models.CASCADE)

    class Meta:
        verbose_name="enigme"
        ordering=['chapitre']

    def __str__(self):
        return self.chapitre.nom + '_'+ str(self.numero)

class EnigmeStatus (models.Model):
    chapitre = models.ForeignKey("Chapitre", on_delete = models.CASCADE)
    numero = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=3)
    '''-1 : plus de tentative, pas de bonne réponse,
        -2 : réponse achetée,
        0:  réponse trouvée
        1,2 ou 3: nb de tentatives restantes'''
    class Meta:
        ordering = ['chapitre']

    def __str__(self):
        return self.user.username + '_' + self.chapitre.nom + '_' + str(self.numero)

class CollapsibleText (models.Model):
    titre = models.CharField(max_length=20, blank=True)
    collapsed = models.BooleanField(default=True)
    contenu = models.TextField()
    conteneur = models.ForeignKey("CollapsibleContainer", on_delete=models.CASCADE)

    def clean(self):
        self.collapsed = True
        return self

    def __str__(self):
        return self.conteneur.titre +' ' +self.titre

class CollapsibleContainer(models.Model):
    titre = models.CharField( max_length=20)

    def __str__(self):
        return self.titre
