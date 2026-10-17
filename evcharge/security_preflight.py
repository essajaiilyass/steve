#!/usr/bin/env python3
"""Read-only warnings for EV CHARGE's upstream SteVe pilot configuration.

Run from any working directory: python3 evcharge/security_preflight.py
No secrets are printed or modified.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILES = [
    ROOT / "src/main/resources/application-docker.properties",
    ROOT / "src/main/resources/application-prod.properties",
]
COMPOSE = ROOT / "docker-compose.yml"


def get_prop(data: str, name: str) -> str | None:
    match = re.search(r"^\s*" + re.escape(name) + r"\s*=\s*(.*?)\s*$", data, re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    warnings = []
    for path in CONFIG_FILES:
        if not path.exists():
            warnings.append(f"{path.name}: fichier manquant")
            continue
        data = path.read_text(encoding="utf-8")
        for field, insecure in (
            ("db.password", {"changeme", "", "password"}),
            ("auth.password", {"1234", "", "admin", "password"}),
        ):
            if get_prop(data, field) in insecure:
                warnings.append(f"{path.name}: {field} est une valeur de démonstration")
        if get_prop(data, "auto.register.unknown.stations") != "false":
            warnings.append(f"{path.name}: enregistrement automatique des bornes à vérifier")
        if get_prop(data, "https.enabled") != "true":
            warnings.append(f"{path.name}: HTTPS intégré non activé (prévoir HTTPS/WSS via proxy sécurisé)")
        if not get_prop(data, "webapi.value"):
            warnings.append(f"{path.name}: API désactivée tant que webapi.value reste vide (normal avant intégration)")
    if not COMPOSE.exists():
        warnings.append("docker-compose.yml: fichier manquant")
    else:
        data = COMPOSE.read_text(encoding="utf-8")
        if re.search(r"^\s*-\s*['\"]?3306:3306['\"]?\s*$", data, re.MULTILINE):
            warnings.append("docker-compose.yml: port de la base 3306 publié")
        if "MYSQL_PASSWORD: changeme" in data:
            warnings.append("docker-compose.yml: mot de passe de démonstration")
        if re.search(r"^\s*-\s*['\"]?8180:8180['\"]?\s*$", data, re.MULTILINE):
            warnings.append("docker-compose.yml: HTTP 8180 publié (ne pas exposer sur Internet)")
    print("EV CHARGE — vérification statique de la configuration SteVe")
    if warnings:
        for warning in warnings:
            print(f"ATTENTION : {warning}")
        print(f"\n{len(warnings)} point(s) à traiter avant tout déploiement public.")
        return 1
    print("Aucun motif connu détecté. Cette vérification ne remplace pas un audit de sécurité.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
