import os
from dotenv import load_dotenv
import requests


# Carga de las variables de entorno desde el archivo .env
load_dotenv()

# Obtener credenciales de la api Spotify desde las variables de entorno

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

url = 'https://accounts.spotify.com/api/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret}

oauth_response = requests.post(url, headers=headers, data=data)

access_token = oauth_response.json().get('access_token')

def search_album(album_name: str):
    
    search_url = 'https://api.spotify.com/v1/search'
    params = {'type': 'album', 'limit': 1, 'q': album_name}
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": "Error al buscar el artista."}
    info_artist = response.json()['albums']['items'][0]['name']
    
    return info_artist

