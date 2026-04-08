#Logging konfigurieren
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

while True:
    try:
        #Daten sammeln
        data = collect_data()
        #Stats speichern
        save_stat(
            data["timestamp"],
            data["cpu"],
            data["ram"],
            data["disk"]
        )

        logging.info(f"Stats gespeichert: CPU={data['cpu']} RAM={data['ram']} Disk={data['disk']}")
        #Warnung prüfen
        warnings = check_thresholds(data)
        #Warnungen speichern
        for warn in warnings:
            timestamp, component, value = warn
            save_warning(timestamp, component, value)
            logging.warning(f"Warnung: {component} = {value}")

        time.sleep(5)
    
    except Exception as e:
        logging.error(f"Fehler im Monitoring: {e}")
        time.sleep(5)

