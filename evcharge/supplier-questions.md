# Demande technique au fabricant — DL-EU008-6

## English message ready to send

Hello,

We have purchased a **DL-EU008-6 22 kW AC EV charger**, advertised with 4G / Wi-Fi, RFID and OCPP 1.6. Charging works when using the two supplied RFID cards.

We are building our own **EV CHARGE** charging management platform and want to connect the charger to our own OCPP central system.

Could you please confirm for **our exact serial number / firmware version**:

1. Does our unit support **OCPP 1.6 JSON over WebSocket (OCPP 1.6J)**, or is OCPP an optional hardware/firmware version?
2. How can we configure a **custom OCPP server URL (ws:// or wss://)** and **ChargeBox ID** without depending on WeGoodCharger?
3. Does it support TLS/WSS, and if yes, which OCPP security profile and certificate configuration?
4. Can the station be controlled using **RemoteStartTransaction**, **RemoteStopTransaction**, and remote RFID authorization?
5. Does it send **BootNotification, Heartbeat, StatusNotification, StartTransaction, MeterValues and StopTransaction**? What is the meter value unit and measurand?
6. Are the two supplied RFID cards stored locally, or authorized through OCPP? Can we add/remove more RFID cards?
7. Can the unit work with an independent OCPP server, without the original manufacturer cloud?
8. Please provide the configuration manual, exact firmware version, and a screenshot/video of the OCPP settings screen.

Thank you.

## À relever sur la borne

- Photo de l'étiquette : référence et numéro de série (conserver en privé).
- Version de firmware et éventuel identifiant ChargeBox ID.
- Type de connexion Internet réellement présent (Wi-Fi ou modem 4G/SIM).
- Photos du menu de configuration OCPP / réseau.
- Résultat d'une recharge avec badge (sans publier les identifiants RFID en clair).

Ne jamais publier sur GitHub les numéros de série associés aux clients, identifiants de badges, mots de passe, tokens, adresses de réseau privées, ni les clés d'API.
