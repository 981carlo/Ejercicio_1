from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from configuration.connection import DatabaseConnection
from spotify_sevice import search_album

app = FastAPI()

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

@app.get("/add_album/{album_name}")
async def get_album(album_name: str):
    
    info = search_album(album_name)
    album_name = info[0]    
    artist_name = info[1]
    
    return (f'El álbum {album_name} del artista {artist_name} ha sido añadido a tu colección.')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)