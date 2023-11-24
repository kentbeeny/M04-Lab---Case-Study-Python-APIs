#Kent Beeny
#SDEV220
#11/23/23
#M04 Lab - Case Study: Python APIs

"""from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#next line fixed error:
#"RuntimeError: Working outside of application context.
#This typically means that you attempted to use functionality that needed
#the current application. To solve this, set up an application context
#with app.app_context(). See the documentation for more information."

#when trying to run "db.create_all()" in CMD

#used info from:
#https://www.reddit.com/r/flask/comments/ykm1w4/dbcreate_all_not_working/
#https://www.youtube.com/shorts/Ah8y8dFx1c8
app.app_context().push()


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __rep__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():
    return{"drinks": "drink data"}


#did this to test when the drinks route was not working
#discovered I just needed to end the session and restart
#@app.route('/yes')
#def yes():
#    return 'Yes'
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#next line fixed error:
#"RuntimeError: Working outside of application context.
#This typically means that you attempted to use functionality that needed
#the current application. To solve this, set up an application context
#with app.app_context(). See the documentation for more information."

#when trying to run "db.create_all()" in CMD

#used info from:
#https://www.reddit.com/r/flask/comments/ykm1w4/dbcreate_all_not_working/
#https://www.youtube.com/shorts/Ah8y8dFx1c8
app.app_context().push()

#define the Book database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

#default index page that just says hello
@app.route('/')
def index():
    return 'Hello!'

"""#leftover from the initial 'drinks' tutorial
#@app.route('/drinks')
#def get_drinks():
#    return{"drinks": "drink data"}
"""

#page that displays all the books in the Book database
@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return{"books": output}

#displaying books by adding the ID to the URL
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    #return jsonify({'name': book.book_name, 'author': book.author, 'publisher': book.publisher})
    return {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}

#creating new books to add to the Book database
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'],author=request.json['author'],publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

#deleting books from the Book database
@app.route('/books/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return{"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "she dun fer"}

"""
did this to test when the drinks route was not working
discovered I just needed to end the session and restart
@app.route('/yes')
def yes():
    return 'Yes'
"""
