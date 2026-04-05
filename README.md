# Hobby Caravan CI-Bus Connectivity

Dieses Python-Skript initialisiert den Hobby CI-Bus über einen USB-zu-Serial Adapter und aktiviert den Datenstream.  
Es dient als Grundlage, um Fahrzeugdaten auszulesen und Geräte wie Licht, Heizung oder Klima über Systeme wie **Loxone** oder **Home Assistant** zu steuern.

---

## Funktionen

- Initialisierung des CI-Bus beim Systemstart  
- Aktivierung des Datenstreams (`!son`)  
- Abruf aller verfügbaren Variablen (`!gvl`)  
- Bereitstellung der Live-Daten über `/dev/ttyUSB0`  
- Vorbereitung für Integration in Loxone / Home Assistant  

---

## Anforderungen

- Raspberry Pi (z. B. 3B, 4, etc.)  
- USB-zu-Serial RS485 Adapter  
  → meist bereits vorhanden bei **Hobby Connect**

### Alternativ

- Kabel beim Hobby Händler  
- oder selbst bauen (RS485 → LSG WLAN Schnittstelle)

### Optional

- Loxone Miniserver  
- Home Assistant  

---

## Hardware Setup

Du benötigst:

- Raspberry Pi  
- RS485 Adapter (USB)  
- Verbindung zum LSG Modul  

### Anschlussmöglichkeiten

**Hobby Connect vorhanden**  
→ Adapter ist bereits verbaut  

**Ohne Hobby Connect**  
→ RS485 Kabel an WLAN/Service-Port des LSG anschließen  

---

## Installation

### Script kopieren

    cp hobby_init_once.py /usr/local/bin/
    chmod +x /usr/local/bin/hobby_init_once.py

---

## Systemd Service (Daemon)

### Service erstellen

    nano /etc/systemd/system/hobby-init-once.service

### Inhalt der Datei

    [Unit]
    Description=Hobby CI-BUS Einmal-Initialisierung beim Boot
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /usr/local/bin/hobby_init_once.py
    Restart=no

    [Install]
    WantedBy=multi-user.target

---

### Service aktivieren

    systemctl daemon-reload
    systemctl enable hobby-init-once.service
    systemctl start hobby-init-once.service

### Status prüfen

    systemctl status hobby-init-once.service

---

## Verbindung zum Bus

Nach der Initialisierung kannst du direkt auf den Bus zugreifen:

    cat /dev/ttyUSB0

Optional gefiltert:

    cat /dev/ttyUSB0 | grep '$'

---

## Ablauf des Scripts

Das Script führt beim Start folgende Befehle aus:

1. System identifizieren  
       !sys

2. Stream stoppen (Reset)  
       !sof

3. Variablen laden  
       !gvl

4. Warten auf vollständige Antwort (`!end`)

5. Stream starten  
       !son

---

## Wichtige Befehle

### Daten lesen

    cat /dev/ttyUSB0

### Beispiel Werte

- `$1` → Strom (A)  
- `$2` → Spannung (V)  
- `$3` → Batterie %  
- `$29` → Frischwasser  
- `$61` → Licht Decke  
- `$73` → Licht Küche  

---

### Schalten (Toggle)

    printf '!tgl:73\r\n' > /dev/ttyUSB0

(Beispiel: Küche Licht)

---

### Wert setzen

    printf '!set:11=22\r\n' > /dev/ttyUSB0

(Beispiel: Temperatur)

---

### Hauptschalter

    printf '!run:31\r\n' > /dev/ttyUSB0

(Main Power Toggle → `$18`)

---

## Integration in Loxone

Verwendung über Plugin:

https://wiki.loxberry.de/plugins/serial_usb_bridge/start

### Beispiel Eingang

    USB-2=\i$2:\i\v

(Spannung)

### Beispiel Ausgang

    USB-2=!tgl:73\r\n

(Licht schalten)

---

## Integration in Home Assistant

- über MQTT oder Serial Bridge möglich  
- Script liefert bereits alle Daten live  

---

## Sicherheitshinweise

- Zugriff auf `/dev/ttyUSB0` nur lokal erlauben  
- Keine direkten Schreibzugriffe ohne Logik (Toggle beachten!)  
- Systembefehle wie `!run:31` vorsichtig verwenden  

---

## Fazit

Dieses Script ersetzt die **Hobby Connect Box** und ermöglicht:

- direkten Zugriff auf den CI-Bus  
- vollständige Steuerung des Fahrzeugs  
- Integration in Smart Home Systeme  

---

## Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**.

---

## Donation

If this project helps you, you can give me a cup of coffee

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/bastyjuice)
