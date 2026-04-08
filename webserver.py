#Imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from db_module import get_recent_stats, get_recent_warnings
# WICHTIG: Die Datei warnings_module.py muss die Funktionen collect_data 
# und check_thresholds enthalten, damit dieser Import klappt!
from warnings_module import collect_data, check_thresholds

# Port festlegen
PORT = 5000

#Request-Handler
class LiveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- Alles hier drunter muss eingerückt sein ---
        stats = get_recent_stats(10)
        warnings = get_recent_warnings(10) # 's' ergänzt

        # Aktuelle Live-Daten sammeln
        current_data = collect_data()
        current_warnings = check_thresholds(current_data)

        # Header senden
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        #HTML-Seite aufbauen
        html = """
        <html>
        <head>
            <title>Pi Monitor Live</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body { font-family: Arial; background-color: #111; color: #eee; padding: 20px; }
                h1 { color: #0f0; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; }
                th { background-color: #222; }
                .warning { color: #f00; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>📊 Live Stats</h1>
            <table>
                <tr><th>ID</th><th>Zeit</th><th>CPU</th><th>RAM</th><th>Disk</th></tr>
        """

        # Historische Stats einfügen
        for row in stats:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}%</td><td>{row[3]}%</td><td>{row[4]}%</td></tr>"
            
        # Aktuelle Live-Daten Zeile (als Teil der Tabelle)
        html += f"<tr class='warning'><td>LIVE</td><td>{current_data['timestamp']}</td><td>{current_data['cpu']}%</td><td>{current_data['ram']}%</td><td>{current_data['disk']}%</td></tr>"
        
        html += """
            </table>
            <h1>⚠️ Warnings</h1>
            <table>
                <tr><th>ID</th><th>Zeit</th><th>Komponente</th><th>Wert</th></tr>
        """

        # Historische Warnungen aus der DB
        for row in warnings:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}%</td></tr>"
            
        # Ganz frische Warnungen (noch nicht in DB)
        for warn in current_warnings:
            timestamp, component, value = warn
            html += f"<tr class='warning'><td>—</td><td>{timestamp}</td><td>{component}</td><td>{value}%</td></tr>"

        html += """
            </table>
        </body>
        </html>
        """
        
        # HTML an den Browser senden
        self.wfile.write(html.encode("utf-8"))

#Damit der Server auch wirklich startet
if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), LiveHandler)
    print(f"Webserver läuft auf http://localhost:{PORT}")
    server.serve_forever()