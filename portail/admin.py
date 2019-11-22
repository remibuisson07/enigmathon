from django.contrib import admin
from .models import Chapitre, Enigme, Joueur, EnigmeStatus, CollapsibleText, CollapsibleContainer, Couleur



# Register your models here.
admin.site.register(Chapitre)
admin.site.register(Enigme)
admin.site.register(Joueur)
admin.site.register(EnigmeStatus)
admin.site.register(CollapsibleText)
admin.site.register(CollapsibleContainer)
admin.site.register(Couleur)
