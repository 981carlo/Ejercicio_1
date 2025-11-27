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