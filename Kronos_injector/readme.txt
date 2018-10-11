Kronos Injector
________________

Script pour injecter des abonnés et leurs abonnements via l'API Kronos sur la base d'un csv.
Contiendra a terme la possibilité d'envoyer des perturbations dans Chaos.


Prérequis
_____________

* Module python Requests
* Fichier config.csv rempli avec les tokens Chaos & Kronos, le contributor, les urls, le coverage et,
si necessaire, un prefixe pour distinguer les abonnés créés par ce script.
* Dans le dossier datasets, deux csv :
    - csv_test_subscribers (external_id, coverage, firstname, lastname)
    - csv_test_subscriptions (owner, address, channel_type, address_type, pt_object, pt_object_type, days,
                 active, monitoring_begin, monitoring_end)



Déroulement
__________

Lancer main.py
Tous les subscribers & leurs subscriptions ont été créées.



Règles:
_______

Si periodes de surveillance mal formatées, elles sont par defaut à 00:00:00 / 23:59:59
Si jours de surveillance mal formatées, ils sont tous en False par defaut.

