import sys
import os

# Aktuellen Ordner zum Python-Suchpfad hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_module import init_db

if __name__ == "__main__":
    init_db()
    print("Datenbank initialisiert!")