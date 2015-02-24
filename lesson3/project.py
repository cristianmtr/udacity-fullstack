from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/')
def editMenuItem(restaurant_id, menuitem_id):
    return "page to edit a menu item. Task 2 complete!"


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/')
def deleteMenuItem(restaurant_id, menuitem_id):
    return "page to delete a menu item. Task 3 complete!"


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
