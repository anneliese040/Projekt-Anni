from http.server import BaseHTTPRequestHandler, HTTPServer
from datenbank import get_recent_stats, get_recent_warnings
from monitor import collect_data, check_thresholds

PORT = 5000

class LiveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            stats = get_recent_stats(10)
            warnings = get_recent_warnings(10)
            current_data = collect_data()
            current_warnings = check_thresholds(current_data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <html>
            <head>
                <title>Pi Monitor Live</title>
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{ font-family: Arial; background-color: #111; color: #eee; padding: 20px; }}
                    h1 {{ color: #0f0; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
                    th {{ background-color: #222; }}
                    .warning {{ color: #f00; font-weight: bold; }}
                </style>
            </head>
            <body>
                <h1>📊 Live Stats (Raspberry Pi Model B)</h1>
                <table>
                    <tr><th>ID</th><th>Zeit</th><th>CPU</th><th>RAM</th><th>Disk</th></tr>
            """
            for row in stats:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}%</td><td>{row[3]}%</td><td>{row[4]}%</td></tr>"
            
            html += f"<tr class='warning'><td>LIVE</td><td>{current_data['timestamp']}</td><td>{current_data['cpu']}%</td><td>{current_data['ram']}%</td><td>{current_data['disk']}%</td></tr>"
            html += "</table><h1>⚠️ Warnings</h1><table><tr><th>ID</th><th>Zeit</th><th>Komponente</th><th>Wert</th></tr>"

            for row in warnings:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}%</td></tr>"
            
            for warn in current_warnings:
                html += f"<tr class='warning'><td>—</td><td>{warn[0]}</td><td>{warn[1]}</td><td>{warn[2]}%</td></tr>"

            html += "</table></body></html>"
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_error(500, f"Server Fehler: {e}")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), LiveHandler)
    print(f"Webserver läuft auf http://<DEINE-PI-IP>:{PORT}")
    server.serve_forever()