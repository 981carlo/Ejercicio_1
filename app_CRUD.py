from fastapi import Request, FastAPI
import mysql.connector

app = FastAPI()

@app.get("/bienvenida_spotify")
async def bienvenida():
    return "¡Bienvenidoas a nuestra API de Spotyfy!"

def make_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2411",
        database="usuarios_spotify"
    )
    return mydb

@app.get("/users")
async def get_users():
    
    mydb = make_connection()    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM usuarios")        
    result = mycursor.fetchall()
    
    return {"Usuarios": result}

@app.post("/users")
async def create_user(request: Request):
    
    mydb = make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    mycursor.execute(f'INSERT INTO `usuarios`(nombre, apellido) VALUES ("{nombre}","{apellido}")')
    mydb.commit()
    
    return f'Usuario: {nombre} {apellido}, creado exitosamente.'

@app.put("/users/{id}")
async def update_user(id: int, request: Request):
    
    mydb = make_connection()
    mycursor = mydb.cursor()
    data = await request.json()
    nombre = data['nombre']
    apellido = data['apellido']
    
    mycursor.execute(f'UPDATE `usuarios` SET nombre="{nombre}", apellido="{apellido}" WHERE id={id}')
    mydb.commit()
    
    return f'Usuario con id {id} actualizado exitosamente.'

@app.delete("/users/{id}")
async def delete_user(id: int):
    
    mydb = make_connection()
    mycursor = mydb.cursor()
    
    mycursor.execute(f'DELETE FROM `usuarios` WHERE id={id}')
    mydb.commit()
    
    return f'Usuario con id {id} eliminado exitosamente.'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)