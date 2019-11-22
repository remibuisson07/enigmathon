from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Chapitre, Enigme, Joueur, EnigmeStatus, CollapsibleContainer, CollapsibleText
from .forms import LoginFormulaire, SignUpFormulaire, ReponseForm, Achat, \
    ModifNameForm, ModifPasswordForm, ModifPseudoForm, CodeForm


# les fonctions auxiliaires ----------------



def sendEmail(receiverAdress, pseudo, code):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    envoi = True
    senderAdress = 'enigmathon@gmail.com'
    password = 'luisaf07'

    # préparation des messages
    message = "J'ai le plaisir de confirmer votre inscription à ENIGMATHON" \
                      "le site qui vous propose de résoudre des énigmes numériques avec Python." \
                      "Pour rappel, votre Pseudo est {}." \
                      "Lors de votre première connexion le code suivant vous sera demandé: {}" \
                      "BIENVENUE et bon jeu!".format(pseudo,code)
    messageHTML = "<p>J'ai le plaisir de confirmer votre inscription à ENIGMATHON, " \
                      "<span style='color: gray; font-style: italic;'>le site qui vous propose de résoudre des énigmes " \
                                                  "numériques avec Python.</span></p>" \
                      "<p>Pour rappel, votre pseudo est <span style='color: blue'>"+ pseudo + "</span>.</p>" \
                      "<p>Lors de votre première connexion le code " \
                      "suivant vous sera demandé: <span style='color: green; font-size: 1.5em;'>" + code + "</p>" \
                      "<p>BIENVENUE et bon jeu!</p>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'ENIGMATHON: confirmation de votre inscription'
    msg['From'] = senderAdress
    msg['To'] = receiverAdress

    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(messageHTML, 'html'))

    # login
    server = smtplib.SMTP(host='smtp.gmail.com', port=25)
    server.starttls()
    server.login(senderAdress, password)

    # envoi du mail avec l'expediteur et les destinataires

    server.sendmail(senderAdress,
                    receiverAdress, msg.as_string())

    server.quit()
    return envoi

# Les vues gérant la connexion et la déconnexion d'un joueur ----------------------------

def connexion(request):
    '''la vue qui gère la connexion d'un joueur'''
    message=""
    confirmation=False


    if request.method == "POST":
        formulaire=LoginFormulaire(request.POST)
        if formulaire.is_valid():
            pseudo = formulaire.cleaned_data['pseudo']
            password=formulaire.cleaned_data['password']
            user=authenticate(username=pseudo, password=password)
            if user:
                joueur=Joueur.objects.get(user=user)
                login(request, user)

                if not joueur.first:
                    return redirect(reverse('PORTAIL'))
                else:
                    confirmation = True

            else:
                message = "<p>Pseudo inconnu et/ou mot de passe erroné, veuillez recommencer</p>" \
                  "<p><em> Mot de passe ou Pseudo oublié ? contactez l'administrateur à enigmathon@gmail.com</em></p>"

    if request.user.is_authenticated:
        if request.method == "POST":
            form = CodeForm(request.POST)
            joueur = Joueur.objects.get(user=request.user)
            if form.is_valid():
                code = form.cleaned_data['code']
                if joueur.code == code:
                    joueur.first = False
                    joueur.save()
                    return redirect(reverse('PORTAIL'))
                else:
                    message = "<p>Code de confirmation inexact. Veuillez recommencer</p>"
                    logout(request)

    formulaire=LoginFormulaire()
    form = CodeForm()


    return render(request, 'portail/connexion.html/', locals())




def deconnexion(request):
    logout(request)
    return redirect('PORTAIL')

def inscription(request):
    '''la vue qui permet à un élève de s'inscrire pour la première fois'''

    import random
    import string

    def codecreate(nb_caracteres):
        caracteres = string.ascii_letters + string.digits
        aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]

        return ''.join(aleatoire)



    message=""
    if request.method=="POST":
        formulaire=SignUpFormulaire(request.POST)
        if formulaire.is_valid():
            pseudo = formulaire.cleaned_data['pseudo']
            prenom = formulaire.cleaned_data['prenom']
            nom = formulaire.cleaned_data['nom']
            adresse = formulaire.cleaned_data['adresse']
            password = formulaire.cleaned_data['password']
            user = User.objects.create_user(pseudo, adresse, password)
            user.first_name=prenom
            user.last_name=nom
            user.is_active=True
            joueur=Joueur(user=user)
            joueur.code=codecreate(6)
            if sendEmail(adresse, pseudo, joueur.code):
                user.save()
                joueur.save()
                message = "Bienvenue <span>{}</span>! Un code de confirmation vous " \
                      "a été envoyé à votre adresse électronique".format(pseudo)
            else:
                message="Désolé, un problème est survenu lors de l'envoi du code de confirmation " \
                        "à l'adresse que vous avez donnée. Veuillez recommencer"


    else: formulaire=SignUpFormulaire()
    return render (request, 'portail/inscription.html', {'formulaire':formulaire, 'message': message })

# la vue de l'accueil
def accueil (request):
    '''la première vue du jeu'''
    from random import randint
    x,y = randint(60, 550), randint(60,500)
    return render (request, 'portail/accueil.html', {'x':x, 'y':y})





#Les autres vues:------------------------------

def portail (request):
    '''la vue du tableau de bord'''
    palmares = Joueur.objects.all().exclude(score=0).exclude(invite=True)[:3]
    user=request.user
    if user.is_authenticated:
        joueur=Joueur.objects.get(user=user)
    if user.is_authenticated and not joueur.first:
            chapitres = Chapitre.objects.filter(niveau__lte=joueur.niveau).order_by('index')
            connect=True
    else:
        chapitres = Chapitre.objects.filter(niveau=1).order_by('index')[:2]
        connect=False
    presentation = CollapsibleContainer.objects.get(titre="Regles")
    texts = CollapsibleText.objects.filter(conteneur=presentation)
    for text in texts:
        text.clean()
        text.save()
    modif = CollapsibleContainer.objects.get(titre="ModifierProfil")
    texts = CollapsibleText.objects.filter(conteneur=modif)
    for text in texts:
        text.clean()
        text.save()
    return render (request, 'portail/tableau_bord.html/', locals())



def presentation (request):
    '''la vue qui présente l'introduction et les conseils aux joueurs'''
    presentation=CollapsibleContainer.objects.get(titre="Regles")
    texts = CollapsibleText.objects.filter(conteneur=presentation)

    for text in texts:
        if text.titre in request.GET:
            text.collapsed = not text.collapsed
            text.save()

    return render (request, 'portail/presentation.html/', {'texts': texts })


def page_enigme(request,id):
    '''la vue qui présente les énigmes d'un chapitre donné'''

    '''récupération/création des modèles pertinents'''
    chapitre = Chapitre.objects.get(id=id)
    backgroundcolor = chapitre.couleurfond.code


    if request.user.is_authenticated:
        joueur = Joueur.objects.get(user=request.user)
    if request.user.is_authenticated and not joueur.first:
        '''joueur CONNECTE '''
        connect=True
        message=""
        message_achat=""
        enigmes=Enigme.objects.filter(chapitre=chapitre).order_by('numero')
        N = 0
        for q in enigmes:
            N += 1
            ES = EnigmeStatus.objects.get_or_create(chapitre=chapitre,
                    numero=q.numero, user=request.user)
        enigme_etats=EnigmeStatus.objects.filter(chapitre=chapitre, user=request.user)

        '''formulaire de réponse'''
        RepForm=ReponseForm(request.POST)

        if RepForm.is_valid():
            rep=RepForm.cleaned_data['reponse']
            num= RepForm.cleaned_data['numero']
            if (num>0) and (num<=N):
                ES = EnigmeStatus.objects.get(chapitre=chapitre, user=request.user, numero=num)
                if ES.status>0:
                    joueur.nb_reponses_donnees+=1
                    if rep == Enigme.objects.get(chapitre=chapitre, numero=num).reponse:
                        message = '<strong>  BRAVO !!</strong>'
                        enigme = Enigme.objects.get(chapitre=chapitre, numero=num)
                        joueur.score += enigme.points
                        joueur.niveau=joueur.level()
                        joueur.date_lastscore = timezone.now()
                        joueur.nb_bonnes_reponses+=1
                        ES.status = 0
                    else:
                        message = "Désolé, ce n'est pas la bonne réponse"
                        ES.status = ES.status-1
                        if ES.status==0: ES.status=-1
                    ES.save()
                    joueur.save()
                else: message="Vous ne pouvez plus répondre à cette question"
            else: message = "Numéro de question non valide"
            return render(request, 'portail/page_enigme.html', locals())

        ''' formulaire d'achat'''
        RepForm = ReponseForm()
        achat=Achat(request.POST)

        if achat.is_valid():
            numero = achat.cleaned_data['numero']
            if (numero > 0) and (numero <= N):
                enigme = Enigme.objects.get(chapitre=chapitre, numero=numero)
                ES = EnigmeStatus.objects.get(chapitre=chapitre, user=request.user, numero=numero)
                if (ES.status == -2) or (ES.status == 0): message_achat="Vous connaissez déjà la réponse!"
                elif joueur.score >= enigme.points:
                    joueur.score -= enigme.points
                    joueur.date_lastscore=timezone.now
                    joueur.save()
                    ES.status = -2
                    ES.save()
                else: message_achat="Vous n'avez pas assez de points pour acheter cette réponse"
            else: message_achat = "Numéro de la question non valide"
            return render(request, 'portail/page_enigme.html', locals())
        achat = Achat()

    else:
        '''VISITEUR'''
        connect=False
        enigmes = Enigme.objects.filter(chapitre=chapitre).order_by('numero')[:2]

    return render(request, 'portail/page_enigme.html', locals())


def page_infos (request):
    ''' la vue qui permet au joueur de lire et de modifier son profil'''
    user = request.user
    if not user.is_authenticated:
        return render (request, 'portail/tableau_bord.html')
    else:
        joueur = Joueur.objects.get(user=request.user)
        joueur.niveau=joueur.level()
        joueur.save()
        if not joueur.nb_reponses_donnees==0:
            reussite = round(joueur.nb_bonnes_reponses/joueur.nb_reponses_donnees*100,1)
        modif = CollapsibleContainer.objects.get(titre="ModifierProfil")
        texts = CollapsibleText.objects.filter(conteneur=modif)
        for text in texts:
            if text.titre in request.GET:
                text.collapsed = not text.collapsed
                text.save()

        changepseudo = ModifPseudoForm(request.POST)
        changepassword = ModifPasswordForm(request.POST)
        changename = ModifNameForm(request.POST)
        if request.method=='POST':
            message = ""
            if changepseudo.is_valid():
                password=changepseudo.cleaned_data['password']
                usertest=authenticate(username=user.username, password=password)
                if usertest:
                    pseudo=changepseudo.cleaned_data['pseudo']
                    usertest=User.objects.filter(username=pseudo)
                    if not usertest:
                        user.username=pseudo
                        user.save()
                        message="Profil modifié avec succès"
                        modif = CollapsibleContainer.objects.get(titre="ModifierProfil")
                        texts = CollapsibleText.objects.filter(conteneur=modif)
                        for text in texts:
                            text.clean()
                            text.save()
                    else:
                        message="Le pseudo " + pseudo + " est déjà pris."
                else:
                    message="Mot de passe incorrect"
                return render (request, 'portail/page_infos.html', locals())
            changepseudo=ModifPseudoForm()

            if changename.is_valid():
                password=changename.cleaned_data['password']
                usertest = authenticate(username=user.username, password=password)
                if usertest:
                    prenom=changename.cleaned_data['prenom']
                    nom = changename.cleaned_data['nom']
                    user.first_name=prenom
                    user.last_name=nom
                    user.save()
                    message = "Profil modifié avec succès"
                    modif = CollapsibleContainer.objects.get(titre="ModifierProfil")
                    texts = CollapsibleText.objects.filter(conteneur=modif)
                    for text in texts:
                        text.clean()
                        text.save()
                else:
                    message="Mot de passe incorrect"
                return render(request, 'portail/page_infos.html', locals())
            changename = ModifNameForm()

            if changepassword.is_valid():
                old_password=changepassword.cleaned_data['old_password']
                usertest = authenticate(username=user.username, password=old_password)
                if usertest:
                    new_password=changepassword.cleaned_data['new_password']
                    password_conf = changepassword.cleaned_data['password_conf']
                    if new_password == password_conf:
                        user.password=new_password
                        user.save()
                        message = "Profil modifié avec succès"
                        modif = CollapsibleContainer.objects.get(titre="ModifierProfil")
                        texts = CollapsibleText.objects.filter(conteneur=modif)
                        for text in texts:
                            text.clean()
                            text.save()
                    else:
                        message="Les deux nouveaux mots de passe ne coincident pas"
                else:
                    message="Ancien mot de passe incorrect"
                return render(request, 'portail/page_infos.html', locals())
            changepassword = ModifPasswordForm()



        return render (request, 'portail/page_infos.html', locals())



def page_python (request):
    ''' la vue qui affiche les informations générales de python ainsi que le memento Hachette'''
    conteneur = CollapsibleContainer.objects.get(titre="Python")
    text = CollapsibleText.objects.get(conteneur=conteneur)
    if text.titre in request.GET:
        text.collapsed = not text.collapsed
        text.save()
    return render(request, 'portail/page_python.html', locals())

def page_enigmathon (request):
    ''' la vue qui affiche les informations générales à propos de Enigmathon'''
    conteneur = CollapsibleContainer.objects.get(titre="A propos")
    text = CollapsibleText.objects.get(conteneur=conteneur)
    return render(request, 'portail/page_enigmathon.html', locals())

def palmares (request):
    '''la vue qui affiche le palmarès complet'''
    listepalmares = Joueur.objects.all().exclude(score=0).exclude(invite=True)
    for joueur in listepalmares:
        joueur.niveau=joueur.level()
        joueur.save()
    return render (request, 'portail/page_palmares.html', {'listepalmares':listepalmares})


