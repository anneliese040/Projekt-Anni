from http.server import BaseHTTPRequestHandler, HTTPServer
# Korrigierte Importe passend zu deinen Dateinamen
from db_module import get_recent_stats, get_recent_warnings
from monitor import collect_data, check_thresholds

# Port festlegen
PORT = 5000

# Request-Handler
class LiveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Daten aus der Datenbank (via db_module.py) holen
            stats = get_recent_stats(10)
            warnings = get_recent_warnings(10)

            # Aktuelle Live-Daten sammeln (via monitor.py)
            current_data = collect_data()
            current_warnings = check_thresholds(current_data)

            # Header senden
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # HTML-Seite aufbauen
            html = f"""
            <html>
            <head>
                <title>Pi Monitor Live</title>
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #111; color: #eee; padding: 20px; }}
                    h1 {{ color: #0f0; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; background-color: #1a1a1a; }}
                    th, td {{ border: 1px solid #444; padding: 12px; text-align: left; }}
                    th {{ background-color: #222; color: #0f0; }}
                    .live-row {{ background-color: #2a2a10; font-weight: bold; color: #ff0; }}
                    .warning-row {{ color: #f44; font-weight: bold; }}
                </style>
            </head>
            <body>
                <h1>📊 System Stats: Raspberry Pi Model B</h1>
                <table>
                    <tr><th>ID</th><th>Zeitpunkt</th><th>CPU Last</th><th>RAM Nutzung</th><th>Disk</th></tr>
            """

            # Historische Stats aus der DB einfügen
            for row in stats:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}%</td><td>{row[3]}%</td><td>{row[4]}%</td></tr>"
            
            # Die allerneuesten Live-Daten markiert anzeigen
            html += f"""
                <tr class="live-row">
                    <td>LIVE</td><td>{current_data['timestamp']}</td>
                    <td>{current_data['cpu']}%</td><td>{current_data['ram']}%</td><td>{current_data['disk']}%</td>
                </tr>
            """
            
            html += """
                </table>
                <h1>⚠️ Warnungen (Threshold > 80%)</h1>
                <table>
                    <tr><th>ID</th><th>Zeitpunkt</th><th>Komponente</th><th>Wert</th></tr>
            """

            # Historische Warnungen aus der DB
            for row in warnings:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}%</td></tr>"
            
            # Falls gerade eine Warnung aktiv ist
            for warn in current_warnings:
                html += f"<tr class='warning-row'><td>AKTUELL</td><td>{warn[0]}</td><td>{warn[1]}</td><td>{warn[2]}%</td></tr>"

            html += """
                </table>
            </body>
            </html>
            """
            
            # HTML an den Browser senden
            self.wfile.write(html.encode("utf-8"))

        except Exception as e:
            # Falls ein Fehler passiert, diesen im Browser anzeigen
            self.send_error(500, f"Interner Fehler: {str(e)}")

# Server Start
if __name__ == "__main__":
    try:
        server = HTTPServer(('0.0.0.0', PORT), LiveHandler)
        print("-----------------------------------------------")
        print(f"Webserver erfolgreich gestartet!")
        print(f"Erreichbar unter: http://localhost:{PORT}")
        print("Oder im Netzwerk unter der IP deines Pi.")
        print("Beenden mit Strg+C")
        print("-----------------------------------------------")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWebserver wird beendet...")
        server.server_close()