# init_db.py
from etl.load.database import create_tables

if __name__ == "__main__":
    print("Inicializando infraestructura de base de datos...")
    create_tables()
    print("Tablas creadas exitosamente.")