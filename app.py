from fastapi import FastAPI, HTTPException  # Importamos las clases FastAPI y HTTPException de la biblioteca fastapi
from pydantic import BaseModel  # Importamos la clase BaseModel de la biblioteca pydantic
from typing import Optional, Text  # Importamos los tipos Optional y Text del módulo typing
from datetime import datetime  # Importamos la clase datetime del módulo datetime
from uuid import uuid4 as uuid  # Importamos la función uuid4 del módulo uuid y le asignamos el alias uuid
import uvicorn  # Importamos la biblioteca uvicorn

app = FastAPI()  # Creamos una instancia de la clase FastAPI y la asignamos a la variable app

posts = []  # Creamos una lista vacía llamada posts para almacenar las publicaciones

# Definimos el modelo Post utilizando la clase BaseModel
class Post(BaseModel):
    id: Optional[str]  # Campo opcional de tipo str que representa el ID de la publicación
    title: str  # Campo requerido de tipo str que representa el título de la publicación
    author: str  # Campo requerido de tipo str que representa el autor de la publicación
    content: Text  # Campo de tipo Text que representa el contenido de la publicación
    created_at: datetime = datetime.now()  # Campo de tipo datetime que representa la fecha y hora de creación de la publicación. Por defecto, se asigna el valor actual.
    published_at: Optional[datetime]  # Campo opcional de tipo datetime que representa la fecha y hora de publicación de la publicación
    published: Optional[bool] = False  # Campo opcional de tipo bool que indica si la publicación está publicada. Por defecto, se asigna el valor False.

@app.get('/')  # Decorador para manejar solicitudes GET en la ruta '/'
def read_root():
    return {"welcome": "Welcome to my API"}  # Devuelve un diccionario con un mensaje de bienvenida

@app.get('/posts')  # Decorador para manejar solicitudes GET en la ruta '/posts'
def get_posts():
    return posts  # Devuelve la lista de publicaciones

@app.post('/posts')  # Decorador para manejar solicitudes POST en la ruta '/posts'
def save_post(post: Post):
    post.id = str(uuid())  # Genera un ID único utilizando la función uuid() y lo asigna al campo id de la publicación
    posts.append(post.dict())  # Convierte el objeto post a un diccionario utilizando el método dict() y lo agrega a la lista posts
    return posts[-1]  # Devuelve la última publicación agregada

@app.get('/posts/{post_id}')  # Decorador para manejar solicitudes GET en la ruta '/posts/{post_id}'
def get_post(post_id: str):
    for post in posts:  # Itera sobre las publicaciones en la lista posts
        if post["id"] == post_id:  # Comprueba si el ID de la publicación coincide con el ID proporcionado
            return post  # Devuelve la publicación encontrada
    raise HTTPException(status_code=404, detail="Item not found")  # Lanza una excepción HTTPException con un código de estado 404 si la publicación no se encuentra

@app.delete('/posts/{post_id}')  # Decorador para manejar solicitudes DELETE en la ruta '/posts/{post_id}'
def delete_post(post_id: str):
    for index, post in enumerate(posts):  # Itera sobre las publicaciones en la lista posts junto con sus índices
        if post["id"] == post_id:  # Comprueba si el ID de la publicación coincide con el ID proporcionado
            posts.pop(index)  # Elimina la publicación de la lista utilizando el método pop() y su índice
            return {"message": "Post has been deleted succesfully"}  # Devuelve un diccionario con un mensaje de éxito
    raise HTTPException(status_code=404, detail="Item not found")  # Lanza una excepción HTTPException con un código de estado 404 si la publicación no se encuentra

@app.put('/posts/{post_id}')  # Decorador para manejar solicitudes PUT en la ruta '/posts/{post_id}'
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):  # Itera sobre las publicaciones en la lista posts junto con sus índices
        if post["id"] == post_id:  # Comprueba si el ID de la publicación coincide con el ID proporcionado
            posts[index]["title"] = updatedPost.dict()["title"]  # Actualiza el título de la publicación en la lista
            posts[index]["content"] = updatedPost.dict()["content"]  # Actualiza el contenido de la publicación en la lista
            posts[index]["author"] = updatedPost.dict()["author"]  # Actualiza el autor de la publicación en la lista
            return {"message": "Post has been updated succesfully"}  # Devuelve un diccionario con un mensaje de éxito
    raise HTTPException(status_code=404, detail="Item not found")  # Lanza una excepción HTTPException con un código de estado 404 si la publicación no se encuentra
