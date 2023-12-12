import json
from flask import Flask, request, jsonify
import sqlite3
import os




os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

# conn = sqlite3.connect('books.db')
# cursor = conn.cursor()

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros
@app.route('/books', methods=['GET'])
def get_all_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return jsonify({'books': books})


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente

@app.route('/books/contar_books_autor_desc', methods=['GET'])
def contar_books_autor_desc():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    cursor.execute('SELECT author, COUNT(*) as book_count FROM books GROUP BY author ORDER BY book_count DESC')
    result = cursor.fetchall()
    conn.close()
    return jsonify({'count_by_author': result})



# 2.Ruta para obtener los libros de un autor como argumento en la llamada


@app.route('/books/por_autor', methods=['GET'])
def get_books_por_autor():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    author = request.args.get('author')
    cursor.execute('SELECT * FROM books WHERE author == ? ;', (author,))
    books = cursor.fetchall()
    conn.close()
    return jsonify({'books_por_author': books})



# 3.Ruta para obtener los libros filtrados por título, publicación y autor

@app.route('/books/filter', methods=['GET'])

def books_filter():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    title = request.args['title']
    published = request.args['published']
    author = request.args['author']
    cursor.execute('''
        SELECT *
        FROM books
        WHERE title = ? AND published = ? AND author = ? ;
    ''', (title, published, author ,))
    books_params = cursor.fetchall()
   
    return jsonify(books_params)



app.run()