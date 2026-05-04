from etl.extract.history import get_recently_played
from etl.transform.history_transform import transform_history, split_history_data
from etl.load.database import insert_tracks, insert_history

LIMIT = 50

def run_pipeline():
    print("--- Iniciando Pipeline de Spotify ---")

    try:
        # 1. Extract
        print("[1/4] Extrayendo datos de Spotify...")
        raw_data = get_recently_played(limit=LIMIT)

        if not raw_data:
            print("No hay reproducciones nuevas. Fin del proceso.")
            return

        # 2. Transform
        print("[2/4] Transformando datos...")
        transformed_data = transform_history(raw_data)

        # 3. Split
        print("[3/4] Separando entidades...")
        tracks, listening_history = split_history_data(transformed_data)

        # 4. Load
        print("[4/4] Cargando en PostgreSQL...")
        insert_tracks(tracks)
        insert_history(listening_history)

        print(f"Pipeline OK - {len(listening_history)} eventos procesados")

    except Exception as e:
        print(f"Pipeline failed: {type(e).__name__} - {e}")
        raise

if __name__ == "__main__":
    run_pipeline()