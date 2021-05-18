from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')
def index():
    first_name = 'John'
    stuff = "This is <strong>Bold</strong> text."
    favourite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template('index.html', first_name=first_name, stuff=stuff, favourite_pizza=favourite_pizza)

'''
safe
capitalize
lower
upper
title
trim
striptags
'''

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internam Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
