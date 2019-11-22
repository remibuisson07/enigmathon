from django import forms
from django.contrib.auth.models import User

# les formulaires de connexion et de déconnexion

class LoginFormulaire (forms.Form):
    '''le formulaire de connexion'''
    pseudo = forms.CharField(label="Pseudo", max_length=16, widget=forms.TextInput(
        attrs={
            'class': 'form-control'}
                    ))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
                    ))

class SignUpFormulaire(forms.Form):
    '''le formulaire d'inscription'''
    pseudo = forms.CharField(label = "Pseudo", max_length=10, widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "10 caractères max"}
                                                    ))
    prenom = forms.CharField(label="votre prénom", max_length=10, required=False, widget=forms.TextInput(
                attrs={
                        'class': 'form-control',
                        'placeholder': "facultatif"}
                             ))
    nom = forms.CharField(label="votre nom de famille", max_length=10, required=False, widget=forms.TextInput(
                 attrs={
                        'class': 'form-control',
                        'placeholder': "facultatif"}
                            ))
    adresse = forms.EmailField(label='votre adresse email du lycée', widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "prenom.nom@lycee-chateaubriand.eu"}
                                    ))

    password = forms.CharField(label="votre mot de passe", widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control'}
                                    ))
    password_conf = forms.CharField(label="veuillez confirmer votre mot de passe", widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control'}
                                    ))

    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        user = User.objects.filter(username=pseudo)
        if user:
            raise forms.ValidationError('Le pseudo "%s" est déjà pris.' % pseudo)
        else:
            return pseudo


    def clean_adresse(self):
        adresse= self.cleaned_data['adresse']
        prefixe, provider = adresse.split("@")
        if not provider == "lycee-chateaubriand.eu":
            raise forms.ValidationError(
                'vous devez utiiser un mail scolaire au format prenom.nom@lycee-chateaubriand.eu')
        else:
            user = User.objects.filter(email=adresse)
            if user:
                raise forms.ValidationError('Un joueur est déjà enregistré à cette adresse')
            else:
                return adresse

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_conf = cleaned_data['password_conf']
        if not password == password_conf:
            raise forms.ValidationError('Les deux mots de passe ne coincident pas')


class CodeForm (forms.Form):
    code = forms.CharField(max_length=6, label='code de confirmation', widget=forms.TextInput(
        attrs={'placeholder': 'XXXXXX',
               'class': 'form-control-1'}
    ))


# les formulaires pour modifier le profil
class ModifPseudoForm (forms.Form):
    password = forms.CharField(label="votre mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
    ))
    pseudo = forms.CharField(label="votre nouveau Pseudo", max_length=10, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "10 caractères max"}
    ))





class ModifPasswordForm(forms.Form):
    old_password = forms.CharField(label="votre ancien mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
    ))
    new_password = forms.CharField(label="votre nouveau mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
    ))
    password_conf = forms.CharField(label="confirmez votre nouveau mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
    ))



class ModifNameForm (forms.Form):
    password = forms.CharField(label="votre mot de passe", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'}
    ))
    prenom = forms.CharField(label="votre prénom", max_length=10, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "facultatif"}
    ))
    nom = forms.CharField(label="votre nom de famille", max_length=10, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "facultatif"}
    ))



# les formulaires de réponses pour chaque énigme

class ReponseForm (forms.Form):
    numero = forms.IntegerField(label="Indiquer le numero de la question", widget=forms.NumberInput(
        attrs={
            'class': 'form-control'}
    ))
    reponse = forms.IntegerField(label="Votre réponse", widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': "entier"}
    ))


class Achat (forms.Form):
    numero = forms.IntegerField(label="Indiquer le numéro de la question", widget=forms.NumberInput(
        attrs={
            'class': 'form-control'}
    ))

