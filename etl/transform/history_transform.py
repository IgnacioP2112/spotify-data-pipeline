from datetime import datetime

def transform_history(raw_items):
    transformed = []

    for item in raw_items:
        track = item["track"]
        
        #  Unir todos los artistas con comas
        artists_list = [artist["name"] for artist in track["artists"]]
        artists_combined = ", ".join(artists_list)

        # Convertir string de fecha a objeto datetime de Python
        # Spotify usa formato: 2023-10-27T12:00:00.000Z
        played_at_str = item["played_at"].replace("Z", "")
        played_at_dt = datetime.fromisoformat(played_at_str)

        data = {
            "track_id": track["id"],
            "track_name": track["name"],
            "artist_name": artists_combined,
            "album_name": track["album"]["name"],
            "played_at": played_at_dt
        }

        transformed.append(data)

    return transformed

def split_history_data(transformed):
    tracks = {}
    history = []

    for item in transformed:
        track_id = item["track_id"]

        if track_id not in tracks:
            tracks[track_id] = {
                "track_id": track_id,
                "track_name": item["track_name"],
                "artist_name": item["artist_name"],
                "album_name": item["album_name"]
            }

        history.append({
            "track_id": track_id,
            "played_at": item["played_at"]
        })

    return list(tracks.values()), history