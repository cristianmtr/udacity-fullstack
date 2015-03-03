# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        return render_template('new.html',
                               restaurant_id=restaurant_id)
    elif request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'],
                               description=request.form['description'],
                               course=request.form['course'],
                               price=request.form['price'],
                               restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash('new menu item created!')
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    if request.method == 'GET':
        thisMenuItem = session.query(MenuItem).filter_by(id=menuitem_id).one()
        return render_template('edit.html', restaurant_id=restaurant_id, \
                               item=thisMenuItem)
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
# DONE
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/',
           methods=['POST', 'GET'])
def deleteMenuItem(restaurant_id, menuitem_id):
    if request.method == 'GET':
        item_name = session.query(MenuItem).filter_by(id=menuitem_id)\
                                           .one().name
        return render_template('delete.html', restaurant_id=restaurant_id, \
                               item_name=item_name, item_id=menuitem_id)
    elif request.method == 'POST':
        thisMenuItem = session.query(MenuItem)\
                              .filter_by(id=menuitem_id).one()
        session.delete(thisMenuItem)
        session.commit()
        output = '''<h1>Item has been deleted</h1></br>'''
        output += '''Go <a href='/restaurants/{}/'>Back</a>'''\
            .format(restaurant_id)
        return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/')
def listOfRestaurants():
    restaurants = session.query(Restaurant)
    output = '<h1>Restaurants</h1></br>'
    for i in restaurants:
        output += '''<a href='/restaurants/{}/'>{}</a></br>'''\
            .format(i.id, i.name)
    return output


@app.route('/')
@app.route('/hello')
def HelloWorld():
    items = session.query(MenuItem).all()
    return render_template('hello.html', items=items)


if __name__ == '__main__':
    # creating db connection
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    #
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
