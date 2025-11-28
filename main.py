import os
from fastapi import FastAPI, session,url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FastApiSessionCacheHandler

app = FastAPI()
app.config['SECRET_KEY'] = os.urandom(64)

client_id = 'a561422a0afb428c994aee4444510435'
client_secret = 'a7ee5060c288459e8b0b80b1e102c556'
redirect_uri = 'http://localhost:8000/callback'
scope = ""
cache_handler = FastApiSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)