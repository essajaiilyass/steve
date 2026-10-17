# EV CHARGE Maroc — Pilote SteVe OCPP 1.6

Ce dossier prépare l'intégration d'une borne **DL-EU008-6**, annoncée comme 22 kW AC triphasée, 4G/Wi-Fi et OCPP 1.6.

> **État au 17/10/2026 :** les badges livrés démarrent la recharge. La présence effective d'un firmware OCPP 1.6J configurable sur l'exemplaire n'est **pas encore vérifiée**. Aucune connexion de borne au serveur n'a été validée.

## Objectif V0 : tester une seule borne, sans paiement

1. Confirmer auprès du fabricant **OCPP 1.6 JSON over WebSocket**, possibilité de changer l'URL du serveur, et accès aux paramètres de la borne.
2. Préparer un serveur SteVe de test (MySQL/MariaDB, Docker, connexion réseau adaptée).
3. Enregistrer manuellement le **ChargeBox ID** dans `Data Management > Charge Points`.
4. Configurer la borne pour joindre le point d'accès OCPP du serveur; confirmer le message `BootNotification` et les `Heartbeat`.
5. Tester successivement `StatusNotification`, l'authentification RFID, `StartTransaction`, `MeterValues`, `StopTransaction`, puis les commandes `RemoteStartTransaction` / `RemoteStopTransaction` **si le contrôleur les prend en charge**.
6. Contrôler que le kWh mesuré correspond aux relevés de la borne et ne présumer d'aucune certification métrologique.
7. Seulement ensuite : relier le backend EV CHARGE/Lovable via une API serveur protégée, jamais depuis une application cliente directement vers l'administration SteVe.

## Premières actions

- Lire [les questions au fournisseur](supplier-questions.md).
- Lire [le protocole de vérification de la borne](acceptance-tests.md).
- Exécuter le contrôle des paramètres par défaut depuis la racine du dépôt : `python3 evcharge/security_preflight.py`.
- Documentation originale de SteVe : [README à la racine](../README.md), [API OpenAPI](../api-docs.json).

## Sécurité : aucun serveur public à cette étape

Le projet SteVe d'origine contient des identifiants d'exemple dans `src/main/resources/application-docker.properties` et `src/main/resources/application-prod.properties`. La configuration `docker-compose.yml` d'origine expose aussi MariaDB via le port 3306.

**Ne pas exécuter ce Compose tel quel sur un serveur public.** La configuration finale devra :

- utiliser de nouveaux secrets privés (base de données, accès administrateur et API), sans jamais les pousser sur GitHub ;
- ne jamais publier le port MySQL/MariaDB (3306) ;
- n'autoriser que les ChargeBox ID connus (`auto.register.unknown.stations=false`) ;
- protéger l'administration par réseau privé/VPN et utiliser HTTPS/WSS pour les échanges depuis Internet selon la compatibilité réelle de la borne ;
- activer la sauvegarde, la journalisation prudente et des restrictions réseau ;
- valider les aspects électriques, les protections et la mesure avant exploitation publique.

**Attention :** les fichiers `.properties` d'origine sont suivis par Git. Modifier leurs mots de passe en place puis faire un commit exposerait les secrets. Les valeurs réelles doivent être injectées pendant le déploiement, depuis un stockage de secrets externe ou des fichiers locaux non versionnés.

Ce dossier contient uniquement la préparation et ne déploie pas de service.
