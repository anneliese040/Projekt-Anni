import logging
import time
import datetime
import psutil
from db_module import save_stat, save_warning

def collect_data():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

def check_thresholds(data):
    warnings = []
    if data["cpu"] > 80:
        warnings.append((data["timestamp"], "CPU", data["cpu"]))
    if data["ram"] > 80:
        warnings.append((data["timestamp"], "RAM", data["ram"]))
    if data["disk"] > 80:
        warnings.append((data["timestamp"], "Disk", data["disk"]))
    return warnings

# Das hier sorgt dafür, dass die Logs nur erscheinen, wenn gewollt
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- DAS IST DIE SCHUTZMAUER ---
if __name__ == "__main__":
    print("Monitoring gestartet... (Beenden mit Strg+C)")
    while True:
        try:
            data = collect_data()
            save_stat(data["timestamp"], data["cpu"], data["ram"], data["disk"])
            logging.info(f"Stats gespeichert: CPU={data['cpu']}% RAM={data['ram']}%")
            
            warnings = check_thresholds(data)
            for warn in warnings:
                timestamp, component, value = warn
                save_warning(timestamp, component, value)
                logging.warning(f"Warnung: {component} = {value}%")

            time.sleep(5)
        except Exception as e:
            logging.error(f"Fehler im Monitoring: {e}")
            time.sleep(5)