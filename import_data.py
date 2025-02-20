from models import init_db
from data_manager import DataManager

def main():
    # Inizializza il database
    init_db()
    
    # Importa i dati
    data_manager = DataManager()
    data_manager.import_from_csv()
    
    print("Importazione completata con successo!")

if __name__ == "__main__":
    main()
