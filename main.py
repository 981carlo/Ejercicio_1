from fastapi import Request, FastAPI
import mysql.connector

app = FastAPI()

@app.get("/bienvenida_spotify")
async def bienvenida():
    return "¡Bienvenidoas a nuestra API de Spotyfy!"
