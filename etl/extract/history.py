import requests
from etl.extract.auth import get_access_token

# URL estandar de la API de Spotify para historial reciente
URL = "https://api.spotify.com/v1/me/player/recently-played"

def get_recently_played(limit=50):
    """
    Obtiene historial reciente de reproducciones.
    Retorna estrictamente la lista cruda de items (JSON/Dict).
    """
    token = get_access_token()
    if not token:
        raise Exception("No se pudo obtener el token de acceso.")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "limit": limit
    }

    response = requests.get(URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Error obteniendo historial: {response.status_code} - {response.text}")

    data = response.json()
    
    # Retornamos solo la lista de reproducciones
    return data.get("items", [])

if __name__ == "__main__":
    # PRUEBA DE EXTRACCION AISLADA
    # Este bloque solo sirve para que tu, como desarrollador, valides que la API responde.
    # No debe haber logica de persistencia ni limpieza aqui.
    try:
        print("Probando extraccion de historial...")
        raw_data = get_recently_played(limit=5)
        print(f"Exito. Se obtuvieron {len(raw_data)} registros crudos.")
        for item in raw_data:
            print(f"ID: {item['track']['id']} - Cancion: {item['track']['name']}")
    except Exception as e:
        print(f"Falla en la prueba de extraccion: {e}")