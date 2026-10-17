# Plan d'essais d'acceptation — première borne EV CHARGE

**Borne pilote :** DL-EU008-6 (22 kW AC annoncés), fonctionnement local par badge déjà confirmé.

Les tests ci-dessous restent **À faire** tant qu'un serveur et une borne ne communiquent pas effectivement.

| Étape | Résultat attendu | Statut |
| --- | --- | --- |
| Identification du firmware | OCPP 1.6J et URL personnalisable documentés | À vérifier |
| Réseau | Borne connectée à Internet via Wi-Fi/4G | À vérifier |
| Connexion WebSocket | Borne reconnue par son ChargeBox ID | À faire |
| BootNotification | Notification de démarrage acceptée par SteVe | À faire |
| Heartbeat | Signal de vie visible dans SteVe | À faire |
| StatusNotification | État du connecteur transmis | À faire |
| Badge RFID | Autorisation acceptée/refusée conformément à la liste serveur | À faire |
| StartTransaction | Identifiant de transaction créé | À faire |
| MeterValues | Énergie remontée avec une unité explicite, sans doublons | À faire |
| StopTransaction | Transaction clôturée et dernier index enregistré | À faire |
| RemoteStartTransaction | Démarrage distant, si pris en charge et avec véhicule raccordé | À faire |
| RemoteStopTransaction | Arrêt distant, si pris en charge | À faire |
| Coupure réseau | Comportement sûr et transactions réconciliées après reconnexion | À faire |
| Coupure électrique | Reprise en état sûr suivant le manuel constructeur | À faire |

## Critères de réussite

Une même session apparaît dans SteVe avec identifiant, début/fin, état du connecteur et index compteur utilisables. Une authentification invalide doit être rejetée conformément aux réglages de la borne. **Aucun démarrage automatique non souhaité** ne doit se produire après une coupure.

Pour un tarif pilote de **3 MAD/kWh**, la facturation sera calculée dans le backend EV CHARGE après validation de la mesure : `montant = kWh facturables × 3`. Aucun prélèvement réel ne doit intervenir à ce stade.

Avant service public : conformité électrique du site, disjoncteur différentiel adapté, protections, mise à la terre, essai de charge réel sous surveillance, fiabilité des mesures et vérifications légales locales.
