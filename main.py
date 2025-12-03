from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from configuration.connection import DatabaseConnection
from spotify_sevice import search_album

app = FastAPI()


# MENSAJE DE BIENVENIDA
@app.get("/")
async def bienvenida():
    
    return "¡Bienvenidoas a nuestra API de Spotyfy!"


# HAY QUE PASAR LOS VALORES DE "user" Y "password" PARA CONECTER CON LA BASE DE DATOS LOCAL
async def make_connection():
    
    mydb = DatabaseConnection(
        host="localhost",
        user="root",
        password="2411",
        database="usuarios_spotify"
    )
    mydb_conn = await mydb.connect_db()        
    return mydb_conn


# ENDPOINT PARA LISTAR USUARIOS
@app.get("/users")
async def get_users():
    
    mydb = await make_connection()    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM usuarios")        
    result = mycursor.fetchall()    
    return {"Usuarios": result}


# ENDPOINT PARA AÑADIR USUARIOS
@app.post("/users")
async def create_user(request: Request):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    if not isinstance(nombre, str) or not isinstance(apellido, str):
        raise HTTPException(status_code=404, detail='El nombre y el apellido deben ser strings')
    
    mycursor.execute(f'INSERT INTO `usuarios`(nombre, apellido) VALUES ("{nombre}","{apellido}")')
    mydb.commit()
    return JSONResponse(content={"message": "Usuario creado exitosamente."}, status_code=201)


# ENDPOINT PARA MODIFICAR USUARIOS
@app.put("/users/{id}")
async def update_user(id: int, request: Request):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    if not isinstance(nombre, str) or not isinstance(apellido, str):
        raise HTTPException(status_code=404, detail='El nombre y el apellido deben ser strings')
    
    mycursor.execute(f'UPDATE `usuarios` SET nombre="{nombre}", apellido="{apellido}" WHERE id={id}')
    mydb.commit()    
    return JSONResponse(f'"message": Usuario con id {id} actualizado exitosamente.', status_code=201)


# ENDPOINT PARA BORRAR USUARIOS 
@app.delete("/users/{id}")
async def delete_user(id: int):
    
    mydb = await make_connection()
    mycursor = mydb.cursor()
    
    mycursor.execute(f'DELETE FROM `usuarios` WHERE id={id}')
    mydb.commit()
    
    return JSONResponse(f'"message": Usuario con id {id} eliminado exitosamente.', status_code=201)


# ENDPOINT PARA BUSCAR ALBUM FAVORITO Y AÑADIRLO AL USUARIO PASADO POR "id"
@app.get("/add_album/{id}/{album_name}")
async def get_album(id: int, album_name: str):
    
    info = search_album(album_name)
    
    if "error" in info:
        
        raise HTTPException(status_code=404, detail="Album no encontrado")
    
    album_name = info[0]    
    artist_name = info[1]

    mydb = await make_connection()
    mycursor = mydb.cursor()
    
    mycursor.execute(f'UPDATE `usuarios` SET album_favorito="{album_name}", artista_favorito="{artist_name}" WHERE id={id}')
    mydb.commit()    
    
    return JSONResponse(content=f'El álbum {album_name} del artista {artist_name} ha sido añadido a tu colección.', status_code=200)

    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)