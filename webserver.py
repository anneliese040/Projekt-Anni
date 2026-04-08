#Imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from db_module import get_recent_stats, get_recent_warnings
from warnings_module import collect_data, check_thresholds

Port festlegen
PORT = 5000

#Request-Handler
class LiveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
    stats = get_recent_stats(10)
    warnings = get_recent_warning(10)

    Aktuelle Live-Daten sammeln
    current_data = collect_data()
    current_warnings = check_thresholds(current_data)


#HTML-Seite aufbauen
html = """
<html>
<head>
    <title>Pi Monitor Live</title>
    <meta http-equiv="refresh" content="2">  <!-- Seite alle 2 Sekunden aktualisieren -->
    <style>
        body { font-family: Arial; background-color: #111; color: #eee; }
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

for row in stats:
    html +=f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"  #Fügt Stats in die Tabelle ein
    html += f"<tr class='warning'><td>—</td><td>{current_data['timestamp']}</td><td>{current_data['cpu']}</td><td>{current_data['ram']}</td><td>{current_data['disk']}</td></tr>" #Fügt live Stats in die Tabelle ein
    html += """
    </table>
    <h1>⚠️ Warnings</h1>
    <table>
        <tr><th>ID</th><th>Zeit</th><th>Komponente</th><th>Wert</th></tr>
"""

for row in warnings:
    html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    
for warn in current_warnings:
    timestamp, component, value = warn
    html += f"<tr class='warning'><td>—</td><td>{timestamp}</td><td>{component}</td><td>{value}</td></tr>"

    html += """
    </table>
</body>
</html>
"""