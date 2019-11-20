## Back-end de la aplicación toDo App programado en python (Carolina Giménez Arias, Noviembre 2019)

# Importación de librerías
from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__) 

# Configuración de la base de datos SQL llamada todo.db (previamente creada desde terminal usando sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/carolgimenezarias/Desktop/todo/todo.db'
db = SQLAlchemy(app) 

class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key = True) # Se crea una variable id para identificar cada tarea
    text = db.Column(db.String(200)) # Se crea la variable texto donde se introducirán las tareas desde la aplicación
    complete = db.Column(db.Boolean)  # Se crea la variable complete para indicar si la tarea se ha completado o no
  
# Configuramos la ruta para cuando no se especifique ninguna url en concreto
@app.route('/') 
def index(): 
    incomplete = Todo.query.filter_by(complete = False).all() 
    complete = Todo.query.filter_by(complete = True).all() 
  
    return render_template('./index.html',  
       incomplete = incomplete, complete = complete) 
  
# Definimos una función para añadir los items que se introduzcan para la lista de quehaceres desde nuestra aplicación
@app.route('/add', methods =['POST']) 
def add(): 
    todo = Todo(text = request.form['todoitem'], complete = False) 
    db.session.add(todo) 
    db.session.commit() 
    return redirect(url_for('index')) # Hacemos que se mantenga en la misma página (home) 
  
# Definimos una función para completar las tareas previamente añadidas
@app.route('/complete/<id>') 
def complete(id): 
    todo = Todo.query.filter_by(id = int(id)).first() 
    todo.complete = True
    db.session.commit() 
    return redirect(url_for('index')) # Hacemos que se mantenga en la misma página (home) 

if __name__ == '__main__': 
    app.run(debug = True)