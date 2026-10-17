# Railway — EV CHARGE OCPP Pilot (préparation sans facturation)

Date : 2026-10-17

## Projet Railway créé

- Nom : `evcharge-ocpp-pilot`
- ID : `1911c70e-6af0-4721-bc4e-13fcd7914f36`
- Environnement : `pilot` (`6edccf03-2264-48c6-a4f6-490358e1b2b0`)
- Accès : https://railway.com/project/1911c70e-6af0-4721-bc4e-13fcd7914f36
- Projet privé ; déploiements automatiques par pull request désactivés.
- **Aucun déploiement, aucun service en exécution et aucun volume provisionné.**

## Modifications Railway préparées (staged uniquement)

| Élément | Identifiant | Configuration préparée |
| --- | --- | --- |
| `steve-ocpp` | `cdaa8d78-f9ff-4d00-a52c-89d8abcff2d3` | Service vide, variables `PORT=8180`, `TZ=UTC` |
| `steve-db` | `90eba26c-2696-4838-bb63-ccbe17b3dde0` | Service vide, variables `MYSQL_DATABASE=stevedb`, `TZ=UTC` |

Ces services sont **en attente d'application** : ils ne possèdent actuellement ni source GitHub attachée, ni image de base de données, ni secrets, ni instance ni stockage. Ils n'impliquent aucune disponibilité réseau ou fonctionnement OCPP.

> Ne pas cliquer sur **Deploy / Apply staged changes** sans autorisation explicite de mise en service et sans finaliser les contrôles suivants.

## Préparation restante avant une première mise en ligne

- Confirmer les détails OCPP 1.6J et la configuration réseau du firmware de la DL-EU008-6.
- Choisir un moteur de base de données compatible SteVe (MySQL 8 ou MariaDB), avec volume **persistant**, sauvegarde et réseau privé Railway **sans port 3306 public**.
- Créer les secrets forts en configuration privée Railway. Ne jamais les écrire dans ce dépôt.
- Préparer l'image/commande de démarrage SteVe : le Dockerfile amont compile à l'exécution et ses fichiers d'application contiennent des identifiants de démonstration. Cette étape nécessite une modification testée pour lire les variables d'environnement et éviter l'utilisation des valeurs par défaut.
- Prévoir un domaine WSS pour les bornes ; protéger l'interface administrateur `/steve/manager` (un simple domaine TLS ne restreint pas l'accès).
- Vérifier compatibilité sous-protocole OCPP et reverse proxy WebSocket.
- Vérifier budget et mise en place d'alertes/limites de consommation Railway.
- Fixer le protocole de validation `BootNotification`, `Heartbeat`, RFID et `MeterValues` ; garder les paiements réels désactivés.

## Source et documents

- Dépôt : `essajaiilyass/steve`
- Branche : `evcharge/pilot-foundation`
- Documentation d'architecture : [railway-deployment.md](railway-deployment.md)
- Liste de recette : [acceptance-tests.md](acceptance-tests.md)
- Sécurité : [README.md](README.md), [security_preflight.py](security_preflight.py)

**Ce fichier n'est ni un manifeste de déploiement automatique ni un certificat de sécurité : il documente uniquement une préparation réversible.**
