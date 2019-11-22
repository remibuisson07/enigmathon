"""enigmes_python_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from portail import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.accueil, name="ACCUEIL"),
    path('admin/', admin.site.urls),
    path('connexion/', views.connexion, name="CONNEXION"),
    path('inscription/', views.inscription, name="INSCRIPTION"),
    path ('deconnexion/', views.deconnexion, name="DECONNEXION"),
    path('portail/', views.portail, name="PORTAIL"),
    path ('portail/presentation/', views.presentation, name="PRESENTATION"),
    path('portail/enigme/<int:id>/', views.page_enigme, name='ENIGME'),
    path('portail/page_infos/', views.page_infos, name='INFOS'),
    path('portail/page_python/', views.page_python, name='PYTHON'),
    path('portail/a_propos/', views.page_enigmathon, name='A PROPOS'),
    path('portail/palmares/', views.palmares, name='PALMARES'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)