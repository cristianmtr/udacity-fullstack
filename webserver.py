from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# sqlalchemy stuff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def post_response_wrapper(s, content):
    s.send_response(301)
    s.end_headers()
    output = ""
    output += "<html><body>"
    output += content
    output += "</body></html>"
    s.wfile.write(output)
    print output
    return


def get_response_wrapper(s, content):
    s.send_response(200)
    s.send_header('Content-type', 'text/html')
    s.end_headers()
    output = ""
    output += "<html><body>"
    output += content
    output += "</body></html>"
    s.wfile.write(output)
    print output
    return


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            if self.path.endswith('/hello'):
                content = "<h1>Hello friends!</h1>"
                get_response_wrapper(self, content)
                return

            if self.path.endswith("/hola"):
                content = '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                get_response_wrapper(self, content)
                return

            if self.path.endswith('/restaurants'):
                output = 'Create a new restaurant \
                <a href="/restaurants/new">here</a>'
                items = session.query(Restaurant).all()
                for item in items:
                    output += '<p>{}'.format(item.name)
                    output += '</br>'
                    output += '<a href="/restaurants/{}/edit">Edit</a></br>'\
                        .format(item.id)
                    output += '<a href="#">Delete</a></br>'
                    output += '</p>'
                get_response_wrapper(self, output)
                return

            if self.path.endswith('/restaurants/new'):
                output = "<h1>New restaurant name?</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'\
                action='/newrestaurant'><input name="new_restaurant_name" \
                type="text" ><input type="submit" value="Submit"> </form>'''
                #
                get_response_wrapper(self, output)
                return

            if self.path.endswith('/edit'):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant)\
                                    .filter_by(id=restaurant_id)[0]
                output = '<h1>{}</h1>'.format(restaurant.name)
                output += '''<form method='POST' enctype='multipart/form-data' \
                action='/restaurants/{}/edit'><input name="new_restaurant_name" \
                type="text"><input type="submit" value="Submit"></form>'''.format(restaurant_id)
                get_response_wrapper(self, output)
                return
                
        except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/newrestaurant"):
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader
                                                ('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get("new_restaurant_name")[0]
                output = ""
                output += "<html><body>"
                # create and commit new restaurant object to db
                new_restaurant = Restaurant(name=new_restaurant_name)
                session.add(new_restaurant)
                session.commit()
                output += "{} has been successfully added to the list.\
                </br>".format(new_restaurant_name)
                output += '<a href="/restaurants">BACK</href>'
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
            if self.path.endswith('/edit'):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant)\
                                    .filter_by(id=restaurant_id)[0]
                ctype, pdict = cgi.parse_header(self.headers.getheader
                                                ('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get("new_restaurant_name")[0]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                restaurant.name = new_restaurant_name
                session.add(restaurant)
                session.commit()
                output = "<p>Restaurant has been modified</p>"
                output += '<a href="/restaurants">BACK</a>'
                post_response_wrapper(self, output)
                return

            else:
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader
                                                ('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</html></body>"
                self.wfile.write(output)
                print output

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    main()
