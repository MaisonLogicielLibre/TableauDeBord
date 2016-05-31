# Installation du projet

## Configuration de l'environnement

 1 - Installation de Python 2.7

```apt-get install python2.7```

 2 - Installation de PIP

```apt-get install python-pip```

 3 - Installation des packages requis

>**WARNING** Si vous êtes sous Windows, supprimer mysql-python du fichier requirements.txt et installer le manuellement depuis [cette page](https://pypi.python.org/pypi/MySQL-python/1.2.5)

```
cd chemin/vers/TableauDeBord/
pip install -r requirements.txt
```

 4 - Installation de django-celery
 
```
easy_install django-celery
```

## Configuration de la base de données

Cet exemple ce base sur l'utilisation d'une table MySQL.

1 - Créer une nouvelle base de données. N.B. Pour ne pas à avoir à changer la configuration par défaut et passer l'étape 2, vous pouvez tout simplement:
 - Créer la base de données `centech_dashboard`
 - Créer l'utilisateur `centech` avec mot de passe `centech`
 - Donner les permissions à l'utilisateur `centech` sur la base de données `centech_dashboard`

2 - Entrez vos paramètres de connexion dans `../TableauDeBord/centech2/settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #Pour utiliser une table MySQL
        'NAME': 'leNomDeLaBaseDeDonnée',
        'USER': 'votreNomDutilisateur',
        'PASSWORD': 'votreMotDePasse',
        'HOST': 'localhost',
    }
}
```
 3 - Mettez à jour votre base de données

 ```
 cd ../chemin/vers/TableauDeBord/
 python manage.py migrate
 python manage.py syncdb
 ```

 4 - Populer votre base de données avec le fichier `../TableauDeBord/populate.sql`
  * Soit en le glissant dans l'encart SQL de votre table MySQL
  * Soit en copiant sont contenu dans l'encart SQL de votre table MySQL

## Configuration de l'application

Entrez les paramètres de votre application dans `../TableauDeBord/centech2/settings.py`

L'email avec lequel envoyé les notifications
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
```

Les constante de votre société et de votre application
```
DASHBOARD_APP = {
    'site': {
        'name': u"",
        'litteral_name': u"",
        'url': u"",
        'dns': u"",
        'email_technique': u"",
        'repository': u"",
        'bugtracker': u"",
        'entreprise': {
            'name': u"",
            'address': u"",
            'phone': u""
        },
        'social': { #Vos réseaux sociaux affiché sur la page d'accueil
            'twitter': u'https://twitter.com/centechmtl',
            'facebook': u'https://www.facebook.com/etscentech?ref=ts&fref=ts',
            'linkedin': u'https://www.linkedin.com/grp/home?gid=2741468&sort=POPULAR',
            'youtube': u'https://www.youtube.com/channel/UCBE0aabDceUdOvd_NtX-jig'
        },
    }
}
```

# Lancement de votre application

A ce stade votre application est déjà opérationnelle. Vous disposez d'un compte administrateur et avez apporter toutes les configurations requises.

1 - Rafraîchir l'image du plan d'étage
```
cd ../chemin/vers/TableauDeBord/
python manage.py updateFloorMap
```

2 - Lancer votre serveur
```
python manage.py runserver
```

3 - Rendez-vous à l'addresse `127.0.0.1:8000` avec votre navigateur

4 - Connectez-vous avec le compte administrateur : 
* Nom d'utilisateur : root
* Mot de passe : root
 
5 - Changez votre mot de passe grâce au menu en haut à droite `menu->Modifier_le_mot_de_passe`.
 
Bienvenue sur votre tableau de bord personnel!

# Configuration de Celery (optionel)

Voir ressource développeur à [cette adresse](https://github.com/CentechMTL/TableauDeBord/wiki/Outils-avec-Django-Celery#configuration-de-celery).
