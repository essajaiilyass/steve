# Déploiement proposé : EV CHARGE OCPP sur Railway

**Statut : proposition uniquement — AUCUN projet Railway déployé ni facturation déclenchée par cette documentation.**

## Architecture pilote

- **Lovable** : interface EV CHARGE (opérateur / clients).
- **Supabase PostgreSQL** : identité utilisateur, rôles, produits, tarification, ventes et états applicatifs. Il ne remplace pas la base de SteVe.
- **Railway — service `steve-ocpp`** : serveur Java 25 SteVe utilisant OCPP 1.6J (WebSocket), avec une configuration de sécurité dédiée au pilote.
- **Railway — service `steve-db`** : MariaDB 10.11.x ou MySQL compatible, stockage persistant, accès UNIQUEMENT sur le réseau privé Railway.
- **Backend EV CHARGE** (Supabase Edge Function / service serveur) : appels authentifiés à l'API SteVe, normalisation des transactions et contrôles d'autorisation. Jamais d'identifiants SteVe dans le navigateur / l'application mobile.

La liaison directe borne → serveur n'est possible que si le **modèle exact DL-EU008-6** expose un client OCPP 1.6J paramétrable avec une URL de serveur externe.

## Vérifications à faire AVANT de lancer des services

1. Confirmer avec le vendeur le firmware OCPP, la procédure d'accès et le `ChargeBox ID`. Une annonce « OCPP 1.6 / 4G ou Wi-Fi » ne confirme pas la configuration livrée.
2. Vérifier les services et régions Railway disponibles, le plan et les limites financières du compte. L'environnement de production n'a pas besoin d'être créé avant validation du budget.
3. Vérifier la compatibilité TLS/WSS de la borne (et éventuelles exigences de certificat / de sous-protocole WebSocket OCPP).
4. Valider la stratégie des **secrets non versionnés** : mots de passe, clés API et accès base doivent exister **uniquement** dans le gestionnaire de secrets Railway.
5. Choisir une authentification et une exposition réseau séparées entre **administration SteVe** et **endpoint WebSocket borne**; ne pas rendre l'administration librement accessible sur Internet.
6. Prévoir un mécanisme de sauvegarde/restauration de MariaDB, surveillance et alertes, mise à jour de SteVe, et limites de coûts Railway.
7. Vérifier les droits et obligations sous licence **GPL-3.0** avant toute redistribution ou personnalisation profonde de SteVe.

## Points techniques propres au dépôt existant

**Attention :** le `docker-compose.yml` du projet amont est prévu pour un test : il utilise notamment le mot de passe `changeme`, publie le port de MariaDB `3306` et celui de l'application en HTTP `8180`.

- Sur Railway, **créer deux services distincts**, ne pas déployer tel quel le `docker-compose.yml`.
- MariaDB/MySQL doit être derrière `*.railway.internal` et conserver ses données dans un **volume persistant**.
- L'application écoute sur `0.0.0.0` (SteVe `application-docker.properties`), port interne `8180`; configurer explicitement le port cible du domaine Railway.
- Déterminer comment SteVe récupère **les secrets de Railway avant toute compilation et au lancement** : le `Dockerfile` amont lance Maven **au démarrage du conteneur**, et les profils Maven exploitent `application-docker.properties` dès le build. Ne pas supposer que des variables Railway sans adaptation suffisent.
- Les paramètres `db.ip`, `db.user`, `db.password`, `auth.user`, `auth.password`, `webapi.value` doivent avoir des valeurs réelles non publiées. Prévoir une adaptation propre du démarrage et tester la priorité des propriétés dans Spring/Maven.
- Garder `auto.register.unknown.stations=false`, et déclarer explicitement le `ChargeBox ID`.
- Point d'entrée de référence documenté par SteVe pour OCPP JSON/WebSocket :
  `/steve/websocket/CentralSystemService` (l'URL finale et la convention d'identifiant devront être testées sur la borne).
- Accès d'administration de référence : `/steve/manager`, à protéger par authentification robuste + filtrage réseau / proxy d'accès distinct.
- Ne jamais partager des informations personnelles ou des clés dans des tickets, captures publiques ou commits GitHub.

## Séquence de déploiement (non exécutée)

1. Créer projet Railway **`evcharge-ocpp-pilot`**, environnement de test.
2. Provisionner la base MariaDB/MySQL avec volume persistant, secret fort, **sans domaine ni proxy TCP public**.
3. Préparer une image SteVe adaptée à Railway et aux secrets d'environnement (après validation du mécanisme Maven/Flyway au démarrage).
4. Connecter le dépôt GitHub `essajaiilyass/steve` sur une branche pilote, déployer le service Java.
5. Tester le démarrage et l'API **sans borne**. Observer logs, consommation RAM/CPU et accès administration restreint.
6. Fournir une URL publique **WSS** pour la seule interface nécessaire aux bornes, avec TLS valide.
7. Renseigner l'ID de borne et essayer `BootNotification` / `Heartbeat` / `StatusNotification` sans autorisation automatique d'un nouvel équipement.
8. Effectuer un test de recharge supervisé via badge, puis tester commandes à distance si prises en charge. Vérifier l'énergie avec l'index de compteur.
9. Intégrer Lovable/Supabase via API serveur, ajouter tarification pilote **3 MAD/kWh**; **paiement réel désactivé** avant validation des mesures et du flux commercial.

## Budget

Railway **Hobby** est affiché à partir de **5 USD/mois**, usage de ressources inclus dans cette somme, avec surcoût si CPU/RAM/stockage/trafic dépassent ce niveau. Ce tarif n'est **pas** une estimation ferme pour deux services fonctionnant 24 h/24. Consulter [Railway Pricing](https://docs.railway.com/pricing) et définir alertes/limites avant activation.

## Décision de mise en production

Pour le pilote, garder la borne sur ses badges actuels tant que la connexion OCPP distante n'est pas validée. Ne pas modifier la configuration de la borne pendant une recharge ou sans possibilité de retour au mode local.
