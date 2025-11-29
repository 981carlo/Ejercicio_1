from dotenv import load_dotenv
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from configuration.connection import DatabaseConnection
import os

# Carga de las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Obtener credenciales de la api Spotify desde las variables de entorno
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')  
redirect_uri = os.getenv('redirect_uri')
scope = os.getenv('scope')

# Iniciar el cliente de Spotify
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

@app.get("/")
async def bienvenida():
    return "¡Bienvenidoas a nuestra API de Spotyfy!"

async def make_connection():
    mydb = DatabaseConnection(
        host="localhost",
        user="root",
        password="2411",
        database="usuarios_spotify"
    )
    mydb_conn = await mydb.connect_db()
    
    return mydb_conn

@app.get("/users")
async def get_users():
    
    mydb = await make_connection()    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM usuarios")        
    result = mycursor.fetchall()
    
    return {"Usuarios": result}

@app.post("/users")
async def create_user(request: Request):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    mycursor.execute(f'INSERT INTO `usuarios`(nombre, apellido) VALUES ("{nombre}","{apellido}")')
    mydb.commit()
    
    return JSONResponse(content={"message": "Usuario creado exitosamente."}, status_code=201)

@app.put("/users/{id}")
async def update_user(id: int, request: Request):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    mycursor.execute(f'UPDATE `usuarios` SET nombre="{nombre}", apellido="{apellido}" WHERE id={id}')
    mydb.commit()
    
    return f'Usuario con id {id} actualizado exitosamente.'

@app.delete("/users/{id}")
async def delete_user(id: int):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    
    mycursor.execute(f'DELETE FROM `usuarios` WHERE id={id}')
    mydb.commit()
    
    return f'Usuario con id {id} eliminado exitosamente.'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)