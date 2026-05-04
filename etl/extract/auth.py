import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

def get_auth_header():
    """Genera el header de autorización base64 requerido por Spotify."""
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {auth_base64}"}

def get_initial_tokens():
    """
    PASO MANUAL ÚNICO: Ejecuta esto solo una vez para obtener tu REFRESH_TOKEN.
    Copia el código que te da y pégalo en tu .env
    """
    import urllib.parse
    scopes = "user-read-recently-played user-top-read"
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scopes
    })
    
    print(f"1. Entra aquí: {auth_url}")
    redirected_url = input("2. Pega la URL de error completa aquí: ")
    code = redirected_url.split("code=")[1]

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=get_auth_header(),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )
    
    data = response.json()
    print("--- TUS TOKENS (Copia el refresh_token en tu .env) ---")
    print(f"ACCESS_TOKEN: {data.get('access_token')}")
    print(f"REFRESH_TOKEN: {data.get('refresh_token')}")

def get_access_token():
    """
    ESTA ES LA FUNCIÓN QUE USARÁ TU PIPELINE.
    Cero inputs, cero humanos. Usa el refresh_token del .env
    """
    if not REFRESH_TOKEN:
        raise Exception(" ERROR: No hay REFRESH_TOKEN en el .env. Ejecuta get_initial_tokens() primero.")

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=get_auth_header(),
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
    )
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f" Error refrescando token: {response.json()}")
        return None

if __name__ == "__main__":
    # Si el .env no tiene el refresh_token, ejecutamos la parte manual
    if not REFRESH_TOKEN:
        get_initial_tokens()
    else:
        # Si ya lo tiene, probamos que el refresco automático funcione
        token = get_access_token()
        if token:
            print(f" Token refrescado automáticamente: {token[:15]}...")