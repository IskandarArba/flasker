from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a Flask Instance
app = Flask(__name__)
# Add Database
# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123asd@localhost/our_users"
# Secret Key!
app.config['SECRET_KEY'] = "my secret key"
# Initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique= True)
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favourite_color = StringField('Favourite Color')
    submit = SubmitField('Submit')

# Create a Form class
class NamerForm(FlaskForm):
    name = StringField('What Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	## Validators
	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf


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


# Create Name Page
@app.route('/name', methods=['POST', 'GET'] )
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('From Submitted Succesfully!!', 'success')

    return render_template('name.html', name=name, form=form)


@app.route('/user/add', methods=['POST', 'GET'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        flash('User Added Succesfully!!', 'success')
    
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Update Database Record
@app.route('/update/<int:id>', methods=['POST', 'GET'] )
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        try:
            db.session.commit()
            flash('User Updated Succesfully!!', 'success')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error!! Looks loke there was a problem.. Please try again', 'danger')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update)
    
