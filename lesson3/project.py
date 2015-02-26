# -*- coding: utf-8 -*-
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        output = '''<form method='POST' enctype='multipar/form-data'\
        action='/restaurants/{}/new/'><h1>Prepare your dish!\
        </h1>'''.format(restaurant_id)
        output += "<strong>Name</strong></br>"
        output += '''<input name="name" type='text'></br>'''
        output += "<strong>Description</strong></br>"
        output += '''<input name="description" type='text'></br>'''
        output += "<strong>Course</strong></br>"
        output += '''<input name="course" type='text'></br>'''
        output += "<strong>Price</strong></br>"
        output += '''<input name="price" type='text'></br>'''
        output += '''<input type='submit' value='Submit'></br>'''
        return output
    elif request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'],
                               description=request.form['description'],
                               course=request.form['course'],
                               price=request.form['price'],
                               restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        output = '''<h1>Your menu item has been created!</h1>'''
        output += '''Go <a href='/restaurants/{}/'>back</a>'''.\
                  format(restaurant_id)
        return output


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    if request.method == 'GET':
        thisMenuItem = session.query(MenuItem).filter_by(id=menuitem_id).one()
        output = '''<form method='POST' enctype='multipar/form-data'\
        action='/restaurants/{}/{}/'><h1>Prepare your dish!\
        </h1>'''.format(restaurant_id, menuitem_id)
        output += "<strong>Name</strong></br>"
        output += '''<input name="name" value="{}" type='text'></br>'''\
            .format(thisMenuItem.name)
        output += "<strong>Description</strong></br>"
        output += '''<input name="description" value="{}" type='text'></br>'''\
            .format(thisMenuItem.description)
        output += "<strong>Course</strong></br>"
        output += '''<input name="course" type='text' value="{}"></br>'''\
            .format(thisMenuItem.course)
        output += "<strong>Price</strong></br>"
        output += '''<input name="price" type='text' value="{}"></br>'''\
            .format(thisMenuItem.price)
        output += '''<input type='submit' value='Edit'></br>'''
        output += '''<a href="/restaurants/{}">Back</a>'''.format(restaurant_id)
        return output
    elif request.method == 'POST':
        thisMenuItem = session.query(MenuItem).filter_by(id=menuitem_id).one()
        thisMenuItem.name = request.form['name']
        thisMenuItem.description = request.form['description']
        thisMenuItem.course = request.form['course']
        thisMenuItem.price = request.form['price']
        session.add(thisMenuItem)
        session.commit()
        output = '''<h1>Your menu item has been edited!</h1>'''
        output += '''Go <a href='/restaurants/{}/'>back</a>'''.\
                  format(restaurant_id)
        return output


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/')
def deleteMenuItem(restaurant_id, menuitem_id):
    return "page to delete a menu item. Task 3 complete!"


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    output = ''
    output += '<h1>{}</h1></br>'.format(restaurant.name)
    for item in items:
        output += "{}</br>".format(item.name)
        output += "Course: {}</br>".format(item.course)
        output += "{}</br>".format(item.description)
        output += "Price: {}</br>".format(item.price)
        # link to edit menu item page
        output += "<a href='/restaurants/{}/{}/'>Edit</a></br>"\
            .format(restaurant_id, item.id)
        output += "</br>"
    # for new menu item POST
    output += "<a href='/restaurants/{}/new/'>Create</a> new item</br>"\
        .format(restaurant_id)
    return output


@app.route('/')
@app.route('/hello')
def HelloWorld():
    output = ""
    items = session.query(MenuItem).all()
    for item in items:
        output += "{}</br>".format(item.name)
        output += "Course: {}</br>".format(item.course)
        output += "{}</br>".format(item.description)
        output += "Price: {}</br>".format(item.price)
        output += "</br>"
    return output


if __name__ == '__main__':
    # creating db connection
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    #
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
