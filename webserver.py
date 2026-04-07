#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import psutil

# Konfiguration
THRESHOLD_CPU = 80.0  # Schwellwert für CPU in Prozent
THRESHOLD_RAM = 80.0  # Schwellwert für RAM in Prozent


def collect_data():
    """
    Sammelt aktuelle CPU- und RAM-Auslastung.
    
    Returns:
        dict: Enthält timestamp, cpu (float), ram (float)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # interval=1 sorgt dafür, dass psutil kurz wartet, um einen Durchschnittswert zu berechnen
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    return {
        "timestamp": timestamp,
        "cpu": cpu_usage,
        "ram": ram_usage
    }


def check_thresholds(data):
    """
    Prüft, ob die gesammelten Werte die Schwellwerte überschreiten.
    
    Args:
        data (dict): Die von collect_data() zurückgegebenen Daten
        
    Returns:
        list: Eine Liste von Tuples (timestamp, component, value) für alle ausgelösten Warnungen.
              Wenn keine Warnungen ausgelöst wurden, ist die Liste leer.
    """
    warnings = []
    
    # CPU prüfen
    if data["cpu"] > THRESHOLD_CPU:
        warnings.append((data["timestamp"], "CPU", data["cpu"]))
        
    # RAM prüfen
    if data["ram"] > THRESHOLD_RAM:
        warnings.append((data["timestamp"], "RAM", data["ram"]))
        
    return warnings

'''
# Optional: Direkte Ausführung zum Testen (wird nicht ausgeführt, wenn das Modul importiert wird)
if __name__ == "__main__":
    print("Teste Datenerfassung...")
    data = collect_data()
    print(f"Gemessene Werte: {data}")
    
    warns = check_thresholds(data)
    if warns:
        print(f"Warnungen gefunden: {warns}")
    else:
        print("Keine Warnungen.")
        '''