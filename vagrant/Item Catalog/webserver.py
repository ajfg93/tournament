from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import restaurant

#sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#sqlalchemy

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith("/hello"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>Hello!"
			output += "<form method = 'POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			return

		if self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>Create new restaurant!"
			output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'><input name='restaurantname' type='text'><input type='submit' value='Create'></form>"
			output += "</body></html>"

			self.wfile.write(output)

			return

		if self.path.endswith("/edit"):
			restID = self.path.split("/")[2]
			myrest = session.query(Restaurant).filter_by(id = restID).one()
			if myrest:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = "<html><body>"
				output += "<h1>"
				output += myrest.name
				output += "</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name='restaurantname' type='text' placeholder = '%s'><input type='submit' value='Rename'></form>" % (myrest.id, myrest.name)
				output += "</body></html>"
				self.wfile.write(output)
			return

		if self.path.endswith("/delete"):
			restID = self.path.split("/")[2]
			myrest = session.query(Restaurant).filter_by(id = restID).one()
			if myrest:	
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = "<html><body>"
				output += "<h1>Are you sure to delete ->"
				output += myrest.name
				output += "</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type='submit' value='Delete'></form>" % myrest.id
				output += "</body></html>"
				self.wfile.write(output)
				return 

		if self.path.endswith("/restaurants"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			rests = session.query(Restaurant).all()

			output = ""
			output += "<html><body>"
			output += "<p><a href='/restaurants/new'>New restaurant</a></p>'"
			for rest in rests:
				output += rest.name + "<br>"
				output += "<a href='/restaurants/%s/edit'>edit</a>" % rest.id + "<br>"
				output += "<a href='/restaurants/%s/delete'>delete</a>" % rest.id + "<br>"
				output += "<br>"

			output += "</body></html>"
			self.wfile.write(output)
			return

		else:
			self.send_error(404, "File Nooooot Found %s" % self.path)

	def do_POST(self):
		if self.path.endswith("/hello"):
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fileds = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fileds.get('message')

				print (type(messagecontent))

				output = ""
				output += "<html><body>"
				output += "<h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]

				output += "<form method = 'POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
			return

		if self.path.endswith("/restaurants/new"):
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fileds = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fileds.get('restaurantname')

				rest_name = messagecontent[0]
				new_rest = Restaurant(name = rest_name)
				session.add(new_rest)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location',  '/restaurants')
				self.end_headers()			

				return 

		if self.path.endswith("/edit"):
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fileds = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fileds.get('restaurantname')

				restID = self.path.split("/")[2]
				myrest = session.query(Restaurant).filter_by(id = restID).one()				

				myrest.name = messagecontent[0]
				session.add(myrest)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location',  '/restaurants')
				self.end_headers()		
			return 

		if self.path.endswith("/delete"):
			restID = self.path.split("/")[2]
			myrest = session.query(Restaurant).filter_by(id = restID).one()		
			session.delete(myrest)
			session.commit()
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.send_header('Location',  '/restaurants')
			self.end_headers()
			return 

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server.."
		server.socket.close()

if __name__ == '__main__':
	main()